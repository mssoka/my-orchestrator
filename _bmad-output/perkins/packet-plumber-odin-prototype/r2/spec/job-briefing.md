# Briefing: packet-plumber-odin-prototype

- **Repo:** Packet-Plumber (`/Users/moses/code/packet-plumber`, remote: `solarity-services/Packet-Plumber`)
- **Worktree:** WORKTREE off `main` (the Odin architecture #15 is on main; isolate). PR targets main.
- **Workflow:** build the Odin early prototype per the Odin architecture. Perkins: **ON** (code — the determinism spine is the ONE hard blocker; otherwise prototype-rigor for the comparison gate, not production-grade). Self-review: bmad-review-edge-case-hunter + bmad-review-verification-gap.
- **Model policy:** **kimi-coding/k3** (the user's preferred coding model — the Odin code goes on kimi).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** ON (code; determinism-spine hard blocker; prototype-rigor otherwise).

## Mission — THE ODIN EARLY PROTOTYPE (Heist 2 of the pivot)

Build the **early Odin prototype** of Packet Plumber in **Odin + Raylib** — re-implement the proven-fun DESIGN (the Godot prototype, on main, is the reference) so the user can **compare it side-by-side with the Godot prototype** (the engine A/B that gates the full game). This is the empirical test of the Odin pivot: does the Odin implementation work, look right, and feel as good (or better) than the Godot one?

## The foundation (read FIRST — the architecture to build from)

1. **`_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md`** (PR #15, ON MAIN) — THE spec. The determinism-native sim core (pure-Odin `core/` package, owned PRNG splitmix64→PCG32 XSH-RR pinned vectors, SOA pools {slot,gen} ids, array-only iteration, arena discipline, headless-safe), the Raylib rendering layer, the golden-image harness (§10), the fun-test systems. **Build EXACTLY to this.**
2. **`_bmad-output/planning-artifacts/gdds/.../gdd.md`** — the engine-agnostic design (Topology, PacketFlow, QoS, Crisis, NetworkHealth mechanics).
3. **`game/` (the Godot prototype, on main)** — the proven-fun REFERENCE. Re-implement the DESIGN (draw pipes, packet flow by type, QoS priority, Network Health, survive the streaming surge), NOT the GDScript code. The fun-test loop must match: playable, the loop closes, win/lose works.
4. **`_bmad-output/planning-artifacts/art-direction/...` (art-direction v1.2)** — the light-canvas visual canon (literal buildings, round capacity-scaled routers, bezier pipes, blue/grey packets, procedural map).

## Build order (per the architecture)

### 1. The golden-image harness FIRST (the verification foundation — §10 of the architecture)
Build the ThePrimeagen-style harness **before the feature systems** — it's how you verify everything else:
- Scripted **demos** (seeded routing scenarios) + **test frames** (time + mouse on a virtual clock).
- **Render-to-texture** → save goldens / compare.
- **Golden compare** (T1 state-hash everywhere + T2 pixel goldens bit-exact via raylib 6.0 rlsw software renderer + PLATFORM_MEMORY).
- **Agent-readable diffs** (pixel diffs you can read to diagnose).
- Every feature below ships with a demo + golden.

### 2. The Simulation Core (Odin — the determinism-native foundation)
- Pure-Odin `core/` package (zero vendor/OS imports, compile-enforced).
- Integer-only sim paths; owned PRNG (splitmix64→PCG32 XSH-RR, pinned reference vectors — NOT core:math/rand); SOA pools {slot,gen} ids; array-only iteration; arena discipline.
- Headless-safe (runs without rendering — the harness + the future leaderboard validator depend on it).

### 3. The fun-test systems (the fun-test loop — re-implement the proven-fun DESIGN)
- **Topology:** nodes (terminals: houses/content-hosts; junctions: routers) + pipes (tiers, span). **Terminal→router-only** (the 'play the internet' topology rule from the Godot prototype).
- **PacketFlow:** packets spawn, route (BFS), flow by type (blue streaming / grey email), terminate at sinks.
- **QoS:** priority lanes (Express/Standard), junction triage (the real decision, NOT the dropped LB toggle).
- **Crisis:** node strain 🟡→🔴 (the warning surface).
- **NetworkHealth:** drains on SLA breach, recharges on health; Error 404 on empty.
- **Router port limits** (canon #14: basic 4 / mid 8 / high 16, one port per pipe) + **router select** (inspect ports/flows + set triage).

### 4. Raylib rendering (light-canvas canon)
- The light Mini Motorways canvas: literal buildings, round capacity-scaled routers, bezier pipes, blue/grey packets, procedural map. Mouse draw, snap-to-node, router select. **Mouse-only** (user ruling).
- **Desktop-first** (user ruling — FORGE #6 amended to sequencing; desktop now, mobile later). **Root layout + game/ removal** via a prototype-fun-gate tag (user ruling).

## User rulings to honor (from the Odin-architecture lavish, session ef5a2724)
- **Desktop-first** launch (FORGE #6 amended to sequencing).
- **Mouse-only** prototype.
- **Root layout + game/ removal** via a prototype-fun-gate tag.
- **1-2 juice stings** at the juice pass.

## Verification (the harness IS the loop — NOT GoPeak)
- Use the **golden-image harness** (§10) as your verification loop: build a feature → scripted demo → render-to-texture → golden compare → **agent-readable pixel diffs** → iterate. This replaces GoPeak (that's Godot-specific).
- Visually verify via the harness's goldens (packet flow, pipe drawing, node health states, Network Health, a crisis + a win) — include them in the lavish.

## Constraints
- **Build to the Odin architecture EXACTLY** (odin-architecture-v1.md) — determinism-native core, owned PRNG, SOA, arena, headless-safe. If you deviate, note why (surface it).
- **Determinism spine is the ONE hard blocker** — a seeded run MUST reproduce (byte-identical state-hash goldens). If determinism breaks, HALT.
- **Re-implement the DESIGN, not the GDScript code** (the Godot prototype is reference for the fun-test loop, not for porting).
- **Mouse-only, desktop-first** (user rulings).
- Em-dashes fine (PP copy).

## Acceptance
- The Odin early prototype RUNS (Odin + Raylib): draw pipes, packets flow by type, QoS works, Network Health reacts, the streaming surge is survivable, Error 404 reachable.
- **The golden-image harness works** (demos run, goldens compare, agent-readable diffs) — built first.
- **Determinism verified** (seeded run reproduces; state-hash goldens byte-identical).
- Visually verified via harness goldens.
- The fun-test loop closes (playable, win/lose) — comparable to the Godot prototype.
- After user review (the engine A/B — play it + compare to Godot): commit, push, open PR targeting main. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set packet-plumber-odin-prototype working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger note packet-plumber-odin-prototype "harness goldens ready: <paths>"` when the harness + first goldens work
- `/Users/moses/code/bin/ledger set packet-plumber-odin-prototype in-review "PR <url>"` when PR opens
- `herdr notification show "odin-prototype" --body "<one-line>"` on finish
- Final message: is it playable (yes/no + what works), the harness state, determinism verified, the goldens, your honest read on Odin vs the Godot prototype (the A/B input), PR URL.

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: packet-plumber-odin-prototype · base: main
