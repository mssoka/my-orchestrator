# Briefing: packet-plumber-v2-1.1-walking-skeleton

- **Standing orders:** Read `/Users/moses/code/docs/orchestration-playbook.md` "Minion standing orders" FIRST — applies in full.
- **Repo:** packet-plumber (`/Users/moses/code/packet-plumber`). **Base: `v2`** (the from-scratch rewrite branch, `82074b8` — NOT main; the prototype code is removed from v2, preserved at `~/code/packet-plumber-prototype-ref` + git history). **PR targets `v2`.**
- **Story:** stories-v2 **Story 1.1 — Walking skeleton (headless spine + harness)**, the first story of slice 1. This is the foundational determinism spine everything else builds on.
- **Workflow:** **gds-dev-story** (implement the story card). Fresh minion. Perkins: **ON** (foundational invariant-heavy code). Self-review: bmad-review-edge-case-hunter (determinism, replay-equality, the no-engine-symbols gate).
- **Model:** `zai-coding-cn/glm-5.2` (kimi down; the ODN rules + the prototype-ref's proven RNG/harness guide the subtlety).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.

## Mission

Build the **headless determinism spine + a fresh golden harness** — the foundation of the from-scratch build. Pure `package core` scaffold + a seeded RNG with pinned test vectors + a state-hash + a binary action-log + a golden-image harness skeleton (software-raylib build, T1 manifest compare, replay gate, one trivial `boot.dem`). **No window yet** (deliberate — lavish sign-off choice 2B: prove the determinism spine headless before any window; the first runnable `app.bin` lands in 1.2). The "launchable increment" for 1.1 is `odin run harness -- run boot` green + `odin test core` green — the headless spine + harness foundation.

## The story (acceptance — from stories-v2 Story 1.1)

**Given** the Odin `package core` scaffold (`Run_State`, `step` no-op, `state_hash`, `log_read`/`log_write`), the owned `Rng` (splitmix64 → PCG32 XSH-RR, ~40 lines, constants in source), and the harness skeleton (`tools/build_raylib_sw.sh` software renderer + memory platform; T1 manifest path `goldens/<demo>.t1`; the replay gate over `log.bin`):

**When** `odin test core` runs the Rng test vectors + the replay-equality test, and `odin run harness -- run boot` replays the trivial `boot.dem` (seed, empty map, N ticks, capture):

**Then:**
- The Rng's first 8 outputs match the pinned vectors `[ODN-9]`.
- Re-stepping `(seed, action_log)` twice yields **byte-identical** `state_hash` sequences `[E10, ODN-10]`.
- `package core` compiles to an object file with **no `vendor:*` / `core:os` / `core:time`** symbols `[ODN-1]`.
- The harness's T1 manifest for `boot.dem` matches on re-run.
- The replay gate reproduces the manifest from the action log alone, and **rejects** catalog / `logic_hz` drift `[ODN-11]`.

**Edge-case contract:** `[E10]` (replay determinism). **Golden:** T1 manifest for `boot.dem` (per-tick FNV-1a-64 hashes, incl rng + events).

## From-scratch mandates
- **Fresh code on `v2`** — do NOT restore or copy the prototype's `core/`/`harness/`. The prototype is **reference-only** at `~/code/packet-plumber-prototype-ref` — mine its RNG implementation (`core/rng.odin`), state-hash/serialize design (`core/serialize.odin`, `snapshot.odin`), and harness shape (`harness/`, `goldens/`) for what worked, but **rebuild clean**.
- **No BFS / no routing yet** — this story is the spine only (Rng + state-hash + action-log + harness). Routing (per-hop/ECMP/bundles) is a later slice.
- **The determinism invariants are load-bearing** — `[ODN-1]` (no engine types in core), `[ODN-9]` (seeded RNG, pinned vectors), `[ODN-10]` (integer-only, no map-iter in core), `[ODN-11]` (state-hash + binary action-log). These are the spine the whole game's replay-equality depends on — get them exactly right.

## Source material (read)
1. **`_bmad-output/planning-artifacts/sprints/stories-v2.md`** — Story 1.1 (full card) + the slice-1 rationale.
2. **`_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md`** — `[ODN-1]` (no engine in core), `[ODN-9]` (seeded RNG), `[ODN-10]` (integer-only/no-map-iter), `[ODN-11]` (state-hash + action-log), `[ODN-17]` (harness), `[E10]` (replay determinism), §11.7 (the headless-test contract).
3. **Prototype reference (read-only):** `~/code/packet-plumber-prototype-ref/core/rng.odin`, `serialize.odin`, `snapshot.odin`, `harness/` (main/replay/goldens), `goldens/` — the proven RNG + harness DESIGN to rebuild from.

## Verify
- `odin test core` green (Rng vectors + replay-equality).
- `odin run harness -- run boot` green; `boot.dem` T1 manifest matches on re-run.
- `package core` object has no `vendor:*`/`core:os`/`core:time` symbols (the ODN-1 gate — verify with `nm`/`odin build` symbol check).
- Replay gate rejects catalog/logic_hz drift.
- After user approval: commit, push, open PR **targeting `v2`** (not main). **Never merge.**

## Self-report (do not skip — set the pr field: `bin/ledger pr <id> <url>`)
- `bin/ledger set packet-plumber-v2-1.1-walking-skeleton working` at start (`clarifying` if you halt)
- `bin/ledger set packet-plumber-v2-1.1-walking-skeleton in-review "PR <url>"` + **`bin/ledger pr packet-plumber-v2-1.1-walking-skeleton <url>`** when PR opens
- `herdr notification show "pp-v2-1.1" --body "<one-line>"` on finish
- Final message: the spine + harness summary, the ODN invariants proven, test/harness results, whether story 1.2 (window + draw one pipe) is the natural next.

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: v2-1.1-walking-skeleton · **base: v2**
- model: zai-coding-cn/glm-5.2 · pr_review: 1 (foundational code; Perkins on glm-5.2 fallback) · github_issue: (none)
- **PR target: v2** (the from-scratch rewrite branch)
