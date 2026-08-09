# Briefing: packet-plumber-prototype-iterate-1

- **Repo:** Packet-Plumber (`/Users/moses/code/packet-plumber`, remote: `solarity-services/Packet-Plumber`)
- **Worktree:** work directly in-repo on a feature branch off `main` (the game code is on main now — #11 merged). PR targets main.
- **Workflow:** prototype iteration (experimental velocity). Perkins: **OFF** (the kimi3 foundation audit + sprint own the rigor; this is fun-test evolution). Use the GoPeak MCP for visual verification (screenshots).
- **Model policy:** deepseek (prototype iteration — NOT kimi3-gated; the full-game sprint waits for kimi3, but prototype evolution continues now).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** OFF (prototype iteration).

## Mission

Iterate the prototype (the fun-test, now on main) with three features the user wants while kimi3's away. Two are CANON (implement per the GDD/epics); one is a NEW experiment (prototype it, flag for canon if fun). **Keep it fun + don't over-complicate** — the user's explicit governor.

## The three features

### 1. 🏠 More locations spawn (CANON — GDD M3 / Epic E3.2)
Nodes appear over time, Mini Motorways-style. Spawn new terminals (houses/content hosts) as the run progresses; unconnected nodes drain Network Health (the demand pressure). Scale spawn rate with time/era. This is the "internet is alive + growing" feel + the kid's explicit ask.
- Per E3.2: "nodes appear over time (Mini Motorways model)." Implement the map-growth director (the architecture's CrisisDirector-driven spawn, seeded/deterministic).
- The player must connect new nodes or suffer Network Health drain — the core growth pressure.

### 2. 🖱️ Select routers (CANON — GDD M2/M3 / Epic E2.3)
Click a router/junction → **inspect + configure**:
- **Inspect:** show its ports (filled/available) + current flows passing through.
- **Configure:** a **priority-policy toggle** (round-robin vs priority) — the junction triage order (E2.3: "per-junction merge/split triage order + LB mode").
- **Keep it light** — a simple panel, not a complex config screen. The fun is the *decision* (which router prioritizes what), not the UI.

### 3. 🔌 Limit router ports by tier (NEW EXPERIMENT — not yet canon)
Routers have a **finite port count** scaling with tier: basic = 4 ports, mid = 8, high = 16 (matching the capacity-scaled router visual — more ports = bigger router). A port is consumed per connected pipe; you can't exceed the router's port count.
- **This is the experiment** — NOT in the GDD/architecture yet. Prototype it. If it's fun (forces meaningful topology decisions without frustration), flag it for a **canon amendment** (the user will decide whether to add it to the GDD/architecture).
- **Ports are GENERIC** (no uplink-vs-user port-type distinction — the user confirmed: pipe tier handles the bandwidth distinction; ports stay simple).
- Governor: don't make it frustrating. The port limit should feel like a meaningful constraint ("this router has 4 ports, choose wisely"), not a punishment.

## Constraints
- **Keep it fun** — the user's explicit priority. Don't over-complicate; the prototype is the fun-test, not production.
- **Visually verify via MCP screenshots** (the GoPeak runtime tools) — confirm new nodes spawn visibly, router selection shows the panel, port limits read clearly. Don't ship features you haven't seen work.
- Follow the locked canon: light canvas, literal buildings, round capacity-scaled routers, blue/grey packets (the art-direction v1.2).
- The determinism spine (ADR-10) must hold — new features (map growth spawn) use the seeded RNG, stay headless-testable.
- Port limits = experimental; clearly flag in your self-report whether it's fun + recommend canon-or-not.

## Acceptance
- Map growth: nodes spawn over time, unconnected = Network Health drain, determinism preserved.
- Router select: click → inspect panel (ports + flows) + policy toggle works.
- Port limits: routers have tier-scaled port counts; can't exceed; your honest read on whether it's fun.
- MCP screenshots verifying each feature.
- After user review (play it): commit, push, open PR targeting main. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set packet-plumber-prototype-iterate-1 working` at start
- `/Users/moses/code/bin/ledger note packet-plumber-prototype-iterate-1 "screenshots ready: <url/paths>"` when features are visually verified
- `/Users/moses/code/bin/ledger set packet-plumber-prototype-iterate-1 in-review "PR <url>"` when PR opens
- `herdr notification show "pp-prototype-iterate-1" --body "<one-line>"` on finish
- Final message: the 3 features, MCP screenshots, your honest fun-read on each (especially the port-limits experiment — fun or frustrating?), whether port limits should become canon, PR URL.

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: packet-plumber-prototype-iterate-1 · base: main
