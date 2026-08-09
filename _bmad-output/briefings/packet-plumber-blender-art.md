# Briefing: packet-plumber-blender-art

- **Repo:** Packet-Plumber (`/Users/moses/code/packet-plumber`, remote: `solarity-services/Packet-Plumber`)
- **Worktree:** WORKTREE off `main` (the main tree is occupied by the prototype-build minion — must isolate). PR targets main.
- **Workflow:** art-direction + **Blender MCP** (the 22-tool server, confirmed working; Blender is running with the addon socket live on :9876). This is ASSET/REFERENCE-RENDER production — use Blender to make the canon concrete. Lavish-gated. Perkins OFF (creative/asset deliverable).
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** OFF.

## Mission

Produce **reference renders + asset prototypes** in Blender that anchor the Packet Plumber visual identity — make the "internet at night, seen from above" aesthetic CONCRETE and visually judgeable. These are the visual target the prototype (2D Godot) + full-game asset production will align to.

**Important framing:** Packet Plumber is a **2D top-down game** (Godot). Blender here produces **concept/reference renders + potentially baked-to-2D assets** — NOT the runtime game engine. The renders establish the LOOK (mood, materials, lighting, the glowing-flow aesthetic); they're the north star for the 2D implementation.

## The canon (read FIRST — this is the spec)

1. **`_bmad-output/planning-artifacts/art-direction/...`** (PR #7, MERGED) — THE visual identity: "the internet at night, seen from above" (dark canvas + glowing flows); streaming = blue #3B82F6, email = grey #B8C0CE (warm reserved for alarms); 9 packet types (color+shape+icon, colorblind-safe); pipes copper→steel→fiber→backbone; textured global map with undersea cables; era evolution (map electrifies).
2. **`_bmad-output/planning-artifacts/narrative/...`** (PR #5, MERGED) — the Dispatcher voice/tone (for any UI/text in the renders).
3. **`_bmad-output/planning-artifacts/gdds/.../gdd.md`** — the world (nodes, packet types, crises, eras).

## Use the Blender MCP (iterate via screenshots)

The Blender MCP is connected (22 tools). Workflow = **build → screenshot → adjust → re-screenshot** (never ship a render you haven't visually verified). Key tools:

- **`blender_execute_blender_code`** — run Python in Blender. **Prefer PROCEDURAL** building for the abstract glowing aesthetic: geometry nodes / emissive materials / bloom for the "glowing flows on a dark canvas" look. This suits the minimalist Mini-Motorways-meets-night aesthetic better than literal realistic models.
- **`blender_get_viewport_screenshot`** — capture each render iteration. This is your verification + the deliverable.
- **Polyhaven search/download** (`blender_search_polyhaven_assets` etc.) — CC0 textures/models/HDRIs IF useful (e.g., a subtle earth/global texture, cable models). Optional — the aesthetic may be cleaner fully procedural.
- **Hyper3D / Hunyuan3D generate** — AI 3D model gen IF a specific prop helps. Optional.

## What to produce (reference renders — the key visual moments)

Render the canon's signature moments so the look is judgeable:

1. **The vista** — the overall "internet at night, seen from above": dark canvas, a cluster of glowing nodes connected by glowing pipes, packets flowing. THE mood shot.
2. **Node identity** — the distinct node types rendered: Residential (house), Content host (server/play), Router/junction (router) — each with a clear icon + glow, colorblind-safe. Source vs sink indicated.
3. **Pipes by tier** — copper (narrow/dim) → steel → fiber (wide/bright) → backbone. The tier-as-visual-language.
4. **Packet flow** — distinct packet types moving along a pipe: blue streaming dots + grey email dots, VISIBLY DIFFERENT (the thing the prototype currently gets wrong — all red).
5. **A crisis moment** — the cable-cut / node-strain arena (the undersea-cable map, a 🟡→🔴 escalation, the alarm warm-color reserved for danger).
6. **(Stretch) Era evolution** — the map "electrifying" across eras (a before/after or progression).

Plus a **concept doc** explaining the materials/lighting/look choices (so the 2D implementation has a recipe to follow).

## Deliverable + placement
- Renders (PNGs) at `_bmad-output/planning-artifacts/art-renders/` (or per a sensible structure).
- A concept/look doc at `_bmad-output/planning-artifacts/art-renders/look-book-v1.md` explaining the aesthetic recipe (materials, lighting, palette in context, how it maps to 2D).
- The `.blend` source file(s) saved (so the work is reproducible/iterable).

## Constraints
- **Follow the canon exactly** (art-direction #7): dark canvas + glowing flows; blue streaming / grey email; warm reserved for alarms; colorblind-safe; Mini Motorways-clean (not realistic/cluttered).
- **Blender must stay running** on the host (the MCP connects to the live instance on :9876). If the connection drops, note it (don't silently fail) — the user keeps Blender open.
- Em-dashes are fine in PP copy (not RT — the briefing-ban was an error).
- Satirical brands only (YouTune/Amazoon/Glitch) — never real trademarks (pre-ship blocker #6).

## Review loop (lavish — BEFORE the PR)
Creative deliverable: render via **lavish** with the renders embedded (the vista, node identity, pipes, packet flow, crisis) + the look-book + post the review URL. The user reacts to the concrete look. Do NOT open the PR until the verdict.

## Acceptance
- Reference renders for the key visual moments (vista, nodes, pipes, packet flow, crisis).
- Packet types VISIBLY distinct (blue vs grey — the prototype's failure mode, done right here).
- A look-book doc (the aesthetic recipe for the 2D implementation).
- `.blend` sources saved.
- After user approval: commit (renders + .blend + look-book), push, open PR targeting main. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set packet-plumber-blender-art working` at start (`clarifying` if you halt — e.g. Blender connection drops)
- `/Users/moses/code/bin/ledger note packet-plumber-blender-art "lavish look-book posted: <url>"` when up
- `/Users/moses/code/bin/ledger set packet-plumber-blender-art in-review "PR <url>"` when PR opens
- `herdr notification show "pp-blender-art" --body "<one-line>"` on finish
- Final message: the renders summary (which moments rendered), the look-book, lavish URL, whether packet-type distinction reads, open questions.

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: packet-plumber-blender-art · base: main
