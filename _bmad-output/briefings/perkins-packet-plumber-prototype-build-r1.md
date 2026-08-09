# Perkins briefing — round 1: packet-plumber-prototype-build

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/11 (targets `main`)
- **Reviewed sha:** `4677f832a499f3b371e6b66ab21fb913ed1fd7ec` (head `packet-plumber-prototype-build`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-prototype-build-r1` — pinned at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-prototype-build.md` + `_bmad-output/planning-artifacts/architecture/architecture-v1.md` (the canon design) + `_bmad-output/planning-artifacts/sprints/sprint-plan-v1.md` (S0–S4). No GitHub issue.
- **prior_findings:** none (round 1).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

The **fun-test prototype** — the playable email→streaming slice (sprint-plan S0→S4) that passed the user's fun-test verdict. This is a **PROTOTYPE**, built for fun-test speed; it may have debt. The briefing's Perkins mandate: **"prototype-appropriate rigor: correctness + the fun-test loop working, not production-grade."** The foundation-audit (a separate job, re-dispatched after this merges) will assess the production-readiness debt — Perkins r1 is about **CORRECTNESS** (does the code work? is the determinism spine intact? are the headless tests real?).

Key systems to verify:
- **Determinism spine (ADR-10):** pure integer-tick headless-safe Simulation Core, separated from Godot rendering; seeded runs reproduce; headless tests exercise the fun-test loop.
- **Core systems:** Topology (nodes + pipes), PacketFlow (packets travel, respect QoS), QoS lanes (streaming/email priority), Crisis (predictable, node states 🟡→🔴), NetworkHealth (loss condition), Era (Email→Streaming transition), the simulation tick.
- **The fun-test loop:** the player can draw pipes, packets flow, priority lanes work, the streaming surge is survivable, Network Health reacts, failure is reachable. MCP-verified via screenshots.
- **Headless tests:** 62/62 green (per the minion's report). Verify they're REAL (not tautologies).

## ⚠️ CRITICAL lens-guard (read before any lens — prevents false positives)

This is a **PROTOTYPE for a fun-test**, not production code. The briefing explicitly scoped Perkins as **"prototype-appropriate rigor: correctness + the fun-test loop working, not production-grade."**

- **Do NOT flag "not production-grade" / "missing features" as blockers.** The prototype is intentionally scoped to S0–S4 (the fun-test slice). S5–S6 (fuller MVP), the full era tree, the leaderboard/meta backend, the AI stress-test system — all deliberately NOT built (the briefing said "stop at the S4 fun-test threshold").
- **Do NOT flag "no leaderboards / no meta-layer / no save system" as missing.** Those are full-game features (S5+), explicitly out of scope for this prototype.
- **Do NOT flag prototype debt (hardcoded values, missing validation, stubbed systems) as BLOCKERS** — note them as warnings/notes only (the foundation-audit owns the debt assessment). The prototype was built for fun-test speed; some debt is expected + acceptable IF the core loop works correctly.
- **Do NOT flag the Godot/GDScript patterns as "wrong language" or "should use C#"** — GDScript is the canon (project-context.md, Godot 4.7.1, gl_compatibility).

### Legitimate findings here would be
- The **determinism spine is compromised** (the sim isn't actually pure/headless-safe/seeded — a seeded run does NOT reproduce; the sim is tangled with the renderer). This is the ONE thing that's a hard blocker (it's the foundation's foundation).
- A **core-loop BUG**: packets don't actually flow, or QoS priority doesn't work, or the surge isn't survivable (the fun-test loop doesn't actually work).
- A **crisis-fairness violation**: crises are random (not design-consequences) — the forge/GDD locked "fair + predictable."
- **Headless tests that are tautologies** (don't actually test the behavior they claim — e.g., assert the thing the code already does, not the constraint).
- A **parse/runtime crash** (the game doesn't run), or a broken Godot project config.
- **Em-dashes in user-facing copy** (PP allows them per the recent clarification — so this is NOT a finding for PP).

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge.
- Save the canonical diff first: `gh pr diff 11 --repo solarity-services/Packet-Plumber` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-prototype-build/r1/diff.patch`. (This is a LARGE diff — the full prototype codebase. Headless mode handles big-diff chunking.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = this briefing + the job briefing + the architecture, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-prototype-build/r1`, `prior_findings` = none (round 1). Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1`), `<lens>.json` + existence check, one retry per failed lens, **big-diff chunking** (this is a big diff — the full prototype), verification pass, consolidation, `consolidated.json`. Close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`): `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)`; on failure fall back to `gh pr comment 11 --repo solarity-services/Packet-Plumber --body-file <body.md>` + note `fallback-comment`; else `GH_TOKEN=$TOKEN gh pr review 11 --repo solarity-services/Packet-Plumber --<event> --body-file <body.md>`.
- Body format:
  ```
  ## 🤖 Perkins automated review — round 1 of 3
  **Job:** packet-plumber-prototype-build · **Reviewed sha:** 4677f83 · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed — <rejected> false-positive[, <u> unverified]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Prototype fun-test (S0-S4): prototype-appropriate rigor (correctness + fun-test loop, not production-grade). Debt noted, not blocked (the foundation-audit owns it)._
  ```
- Before posting, re-fetch `headRefOid`. If it moved, post anyway + note "reviewed `4677f83`, head now `<new>` — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-prototype-build-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5.
