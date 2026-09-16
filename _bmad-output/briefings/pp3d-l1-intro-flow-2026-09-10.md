# PP3D — L1 intro flow (phase A: fork-independent beats)

## User vision (verbatim excerpts, 2026-09-10)

- "in the odin version we have the sites pop out, with animation. so we don't start the level with all the buildings in place. so on start up there shouldn't be any building."
- "the level 1 planet is shown. the begin overlay stays in place. but we give them a bit of history, in a fun way. like 'Did you know how the internet started?' As they begin... UCLA should pop up. then the other site. as we present the text on screen. then we tell them to connect."
- "we don't need them to type anything. just something like now click transmit to send the first message, like we already have. but no traffic flows until they click transmit and then it breaks before it reaches the destination. dropped at the router where it historically dropped if we have the info. then retransmit would start the flow as we have it."

## Scope — PHASE A (fork-independent; the router/inventory question is FENCED OUT)

1. **Empty start:** L1 boots with NO buildings placed. Sites spawn in with pop-out animation per the authored intro script (reference the Odin version's pop-out feel; Godot-native implementation here).
2. **BEGIN overlay + history beat:** the existing begin overlay stays; add the fun history beat — "Did you know how the internet started?" (1969, ARPANET) presented as short on-screen text tied to the spawn beats.
3. **Site sequence:** UCLA pops up first as the text presents it; then the second site (SRI per ARPANET history — verify against canon/spec-l1-arpanet.md and the existing l1_arpanet scene; keep names/history truthful to canon).
4. **Guided connect:** prompt the player to connect the two sites (existing node-to-node drag connect; tutorial guidance text/highlight).
5. **Transmit gate:** no traffic flows until Transmit is clicked; no typing (matches existing behavior — keep).
6. **The historical drop:** the first transmission breaks before reaching the destination — dropped where it historically dropped (the 1969 "LO" crash — canon says scripted, not simulated; stage the drop accordingly, with the text beat explaining what just happened).
7. **Retransmit** starts the normal flow (existing behavior).

## PHASE B — DECIDED (user ruling 2026-09-10, ~16:5xZ)

"maybe the first 2 buildings spawn with routers and the next 2 for level 1 do not."

- **Sites 1–2 (UCLA, SRI)** spawn WITH routers pre-installed — the first connection is pure story + connect + transmit (phase A flow untouched).
- **Sites 3–4** spawn WITHOUT routers — this is where the inventory materializes. (Historically ARPANET's first four nodes were UCLA, SRI, UCSB, Utah — verify canon/spec before naming sites 3–4.)
- **Inventory UX:** materializes when site 3 pops in — slim bottom-center bar (Mini-Motorways discipline, styled to the game's world materials, auto-hides when empty): router icon ×4 (low-tier) + cable/fibre/pipe stock. Player drags routers from inventory onto sites 3 & 4, then connects (existing drag). Top-corner placement is the documented alternative if the bottom bar reads badly in the vision check — decided on screenshots, not another meeting.
- **Aesthetics guard (user):** must not sacrifice the aesthetics/rich world — the inventory appears only when needed and never covers the planet's hero moments.

## Models / bounds

- glm-5.3 @ max (quota-hold regime; k3 available). vision-read skill for look checks. Any godot execution (suite, captures) gated on the user's pending bounded-run authorization — build + static + tests written first.
- Amends the merged L1 (PR #11). pr_review=1, focused PR to main, user merges.
- coordinate_with: packet-plumber-3d-constellation-view (pS8) — shared HUD/level_base surface; keep diffs disjoint, expect the later PR to rebase on the earlier merge.
- No OpenAI, no Blender, no inventory work, no S47/Selva crossover.

## Dispatch parameters

- job_id: packet-plumber-3d-l1-intro-flow
- repo: packet-plumber-3d · repo_root: /Users/moses/code/packet-plumber-3d · github_repo: solarity-services/Packet-Plumber-3D
- slug: l1-intro-flow · base: main (post-#24 head)
- model: zai-coding-cn/glm-5.3 · thinking: max · pr_review: 1
- Skills: bmad-build (mandatory gate; ambiguous-short-config halt → job-local qualified-token binding per gemini-storyboard-internal-unblock-2026-09-10.md), gds-quick-dev, vision-read for captures once authorized.
