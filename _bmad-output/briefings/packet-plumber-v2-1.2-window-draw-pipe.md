# Briefing: packet-plumber-v2-1.2-window-draw-pipe

- **Standing orders:** Read `/Users/moses/code/docs/orchestration-playbook.md` "Minion standing orders" FIRST — applies in full.
- **Repo:** packet-plumber (`/Users/moses/code/packet-plumber`). **Base: `v2`** (`8a564f4` — story 1.1's determinism spine + harness are now IN v2). **PR targets `v2`.**
- **Story:** stories-v2 **Story 1.2 — Window + static render + draw one pipe** (the first runnable `app.bin`).
- **Workflow:** **gds-dev-story**. Fresh minion. Perkins: **ON** (code + the first render/draw path). Self-review: bmad-review-edge-case-hunter.
- **Model:** `zai-coding-cn/glm-5.2` (kimi down).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.

## Mission

Ship the **first runnable `app.bin`**: a 1280×720 window rendering a hardcoded static map, where the player can **draw one pipe** (node→node, snap, cost) and watch it appear. This is the first thing you can *see + touch* — slice 1's playable surface begins here (1.1 was headless by design; 1.2 opens the window).

## Carry-forwards
- **Story 1.1 is merged in `v2`** — the determinism spine (`Run_State`, `step`, `state_hash`, the owned `Rng`, the action-log) + the golden harness (T1 manifest, replay gate) are your foundation. Build ON them; don't redo.
- **W1 from #21 (fold in):** add the **CI-exercised drift-rejection negative test** — a CI assertion that feeds a deliberately-drifted action log and asserts the replay gate REJECTS it (the #599-r2 / verification-gap lesson: the gate's "rejects drift" must be proven in CI, not just locally). Land it with this story's harness work.
- **Routing note:** this story is topology + draw only — **no packet flow yet** (that's 1.3) and **no routing decision** (per-hop/ECMP/bundles comes with flow). Don't pre-build routing.

## The story (from stories-v2 Story 1.2 — read the full card)
- **Slice 1 · Epics E1.1, E1.2 · Systems:** Topology (S1 minimal), Command_Bus, render/view.
- **Goal:** first runnable `app.bin` — 1280×720 window, hardcoded static map, draw one pipe (drag node→node, snap, cost), re-rendered frame matches the **T2 pixel golden**.
- Build the minimal `Topology` (node + pipe data model), the `Command_Bus` (draw command, validation, apply), and the raylib render/view loop on top of the 1.1 spine.

## From-scratch mandates
- **Fresh code on `v2`** — prototype is **reference-only** at `~/code/packet-plumber-prototype-ref` (mine `app/render/` + `core/topology.odin` for the render + topology DESIGN, rebuild clean).
- **Keep the determinism invariants** — the draw/apply path must route through the action-log + state-hash (replay-equality holds: a recorded draw sequence reproduces byte-identical frames). No engine types leaking into `package core`.
- **Golden:** a **T2 pixel golden** for the drawn-frame state (the harness captures + the replay gate verifies).

## Source material (read)
1. **`_bmad-output/planning-artifacts/sprints/stories-v2.md`** — Story 1.2 (full card).
2. **`_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md`** — S1 Topology, the Command_Bus, §11.7 headless-test contract, the ODN spine (carried from 1.1).
3. **`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md`** — E1.1 (node+pipe model), E1.2 (draw interaction — drag, snap, cost).
4. **Prototype reference (read-only):** `~/code/packet-plumber-prototype-ref/app/render/`, `core/topology.odin`.

## Verify
- `app.bin` launches (1280×720), renders the static map, lets you draw one pipe (snap + cost), and the re-rendered frame matches the T2 pixel golden.
- Replay-equality holds over a draw sequence (recorded actions reproduce byte-identical frames).
- The W1 CI drift-rejection negative test is green (the gate rejects a drifted log in CI).
- `odin test` + `odin run harness` green; core still has no engine symbols.
- After user approval: commit, push, open PR **targeting `v2`**. **Never merge.**

## Self-report (set the pr field: `bin/ledger pr <id> <url>`)
- `bin/ledger set packet-plumber-v2-1.2-window-draw-pipe working` at start
- `bin/ledger set packet-plumber-v2-1.2-window-draw-pipe in-review "PR <url>"` + `bin/ledger pr packet-plumber-v2-1.2-window-draw-pipe <url>`
- `herdr notification show "pp-v2-1.2" --body "<one-line>"` on finish
- Final message: the window + draw summary, the T2 golden, the W1 CI test, whether 1.3 (one packet flows) is next.

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: v2-1.2-window-draw-pipe · **base: v2**
- model: zai-coding-cn/glm-5.2 · pr_review: 1 · github_issue: (none)
- **PR target: v2**
