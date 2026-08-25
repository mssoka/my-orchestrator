# Briefing: packet-plumber-v2-1.4-win-lose-stub

- **Standing orders:** Read `/Users/moses/code/docs/orchestration-playbook.md` "Minion standing orders" FIRST — applies in full.
- **Repo:** packet-plumber (`/Users/moses/code/packet-plumber`). **Base: `v2`** (1.1 spine + 1.2 window/draw + 1.3 per-hop flow are IN v2). **PR targets `v2`.**
- **Story:** stories-v2 **Story 1.4 — Win/lose stub (the thinnest feedback loop)**. **Closes slice 1** — draw → flow → survive/fail → retry.
- **Workflow:** **gds-dev-story**. Fresh minion. Perkins: **ON**. Self-review: bmad-review-edge-case-hunter (determinism over the loop, the terminal-event barrier).
- **Model:** `zai-coding-cn/glm-5.2` (kimi down).
- **bmad-quirk heads-up:** verify every edit lands in YOUR worktree (`git status` from cwd); commit/push/PR from the worktree only.

## Mission

Add the **win/lose feedback loop** — the thinnest end-to-end game loop. A packet reaches the sink (win/score) or the run fails (lose/game-over), with a **restart**. This **closes slice 1**: after 1.4, slice 1 is a complete (thin) playable loop — the foundation every later slice grows onto. (It's a STUB — full surge/win-lose depth is slice 4; 1.4 is just the loop skeleton.)

## Carry-forwards
- **1.1** — determinism spine (`Run_State`, `step`, `state_hash`, action-log) + harness. The loop MUST be replay-determinate.
- **1.2** — window + render + topology + draw.
- **1.3** — per-hop packet flow (a packet flows source→router→sink). 1.4 adds: the packet **arriving at the sink = win/score**, and a **lose condition + game-over + restart**.
- **Locked routing already in** (1.3) — no routing work here; 1.4 is the app-mode/feedback layer.

## The story (from stories-v2 Story 1.4 — read the full card)
- **Slice 1 · Epic E6 (stub) · Systems:** App mode FSM `[ODN-13]`, game-over/restart, the terminal-event barrier.
- **Goal:** a packet delivered scores; a lose condition ends the run → game-over frame → restart resets to a fresh seed. The **terminal-event barrier** emits exactly one terminal event (so the golden captures a clean terminal state, not a mid-transition one).

## From-scratch mandates
- **Fresh code on `v2`** — prototype is **reference-only** at `~/code/packet-plumber-prototype-ref` (mine its app FSM/game-over DESIGN, rebuild clean).
- **Determinism holds** — win/lose/restart route through the action-log + state-hash; a recorded loop reproduces byte-identical frames (including the terminal/game-over frame).
- **No engine types in `package core`** (ODN-1).
- **Golden:** the terminal/game-over frame matches a T2 golden; the terminal-event barrier emits exactly one terminal event.

## Source material (read)
1. **`_bmad-output/planning-artifacts/sprints/stories-v2.md`** — Story 1.4 (full card).
2. **`_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md`** — `[ODN-13]` App mode FSM, the terminal-event barrier, §11.7 headless-test contract.
3. **`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md`** — E6 (win/lose — stub level here; full depth is slice 4).
4. **Prototype reference (read-only):** `~/code/packet-plumber-prototype-ref/app/` (FSM/game-over design).

## Verify
- A delivered packet scores; a lose condition → game-over frame → restart resets cleanly (fresh seed).
- Replay-equality over a full loop incl. the terminal frame (bit-for-bit); T2 golden for game-over matches.
- The terminal-event barrier emits exactly ONE terminal event.
- `odin test` + `odin run harness` green; core still engine-free.
- After user approval: commit, push, open PR **targeting `v2`**. **Never merge.**

## Self-report (set the pr field: `bin/ledger pr <id> <url>`)
- `bin/ledger set packet-plumber-v2-1.4-win-lose-stub working` at start
- `bin/ledger set packet-plumber-v2-1.4-win-lose-stub in-review "PR <url>"` + `bin/ledger pr packet-plumber-v2-1.4-win-lose-stub <url>`
- `herdr notification show "pp-v2-1.4" --body "<one-line>"` on finish
- Final message: the loop summary, the slice-1-closure confirmation (draw→flow→survive/fail→retry playable end-to-end), whether slice 2 is next.

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: v2-1.4-win-lose-stub · **base: v2**
- model: zai-coding-cn/glm-5.2 · pr_review: 1 · github_issue: (none)
- **PR target: v2**
