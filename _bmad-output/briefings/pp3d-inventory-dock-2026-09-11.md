# PP3D — inventory dock (Mini Motorways discipline, planet materials)

## User rulings (2026-09-11, design session)

1. Router inventory icons use the SAME SHAPE as the actual 3D router assets — derived silhouettes/renders are fine (not the literal asset), but the three kinds stay distinguishable by their real shapes.
2. Links (1 / 10 / 100 Gbps) must be aesthetically pleasing and fit the planet theme — thickness-coded tiers in the game's own material palette (copper / teal / fibre-with-bright-core), consistent with the pipe/cable language on the map.
3. Quantities: Mini Motorways style — the number OVERLAPS the icon corner; NO "×" character.
4. Overall: the bottom-center dock, MM's layout discipline, the game's dark-glass + brass material world — not a flat-gray MM clone.

## Scope

- **Dock**: bottom-center segmented tray (ROUTERS | divider | LINKS), slide-in on unlock (progressive disclosure preserved), current single-chip behavior replaced.
- **Router slots**: 3 — icons derived from the actual router 3D assets (orthographic renders via the capture harness or traced silhouettes), shape-true per kind, count badge overlapping the corner (no ×), dim at zero, restock pulse if applicable.
- **Link slots**: 3 — 1/10/100 Gbps; thin/medium/thick with copper/teal/fibre-glow coding in the game palette; same count-badge convention.
- **Interaction**: drag-out-to-place with ghost preview (MM muscle memory); links place via the existing connect flow.
- **Bug**: the router item currently does not appear in the inventory at all (only the spool renders) — root-cause and fix; placed routers must read at zoom (small ring/mast emphasis or equivalent — legibility pass).
- **Aesthetic gate**: capture→vision (glm-5.3-flash route) iteration loops; the user's eye is final. Do not ship without captures.

## Models / bounds

- glm-5.3 @ max. No OpenAI. pr_review=1, focused PR to main, user merges. Capture-class entries: windowed allowed, caffeinate wrapper for unattended runs, 900s bound, receipts, stop-on-surprise.
- Skills: bmad-build (mandatory gate; ambiguous-short-config → job-local qualified-token binding per gemini-storyboard-internal-unblock-2026-09-10.md), gds-quick-dev, vision-read for the iteration loop.

## Dispatch parameters

- job_id: packet-plumber-3d-inventory-dock
- repo: packet-plumber-3d · repo_root: /Users/moses/code/packet-plumber-3d · github_repo: solarity-services/Packet-Plumber-3D
- slug: inventory-dock · base: main (current head, post-#32)
- model: zai-coding-cn/glm-5.3 · thinking: max · pr_review: 1
