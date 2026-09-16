# PP3D — constellation view: flattened-planet map (all levels)

## User vision (verbatim, 2026-09-10)

- "we need to enable the constellation view... the tiny planet become flat... we want to keep the animation and look. the difference is that we just see a flat map. this would apply to all levels. so we can structure the folders and scenes appropriately."
- "i expect the flattened map to basically be an exact copy of the tiny planet. it's just split opened and flattened."
- A button toggle was the user's suggested affordance.

## Canon amendment (this PR carries it)

GDD D5a (2026-09-05) scoped the player-triggerable constellation/flattening mode to ADVANCED-era levels (E8.5). USER WIDENING 2026-09-10: the view applies to **ALL levels** from L1 up. Update the GDD + decision-log accordingly (correct-course style amendment, attributed to this ruling). The between-eras campaign-map constellation re-scope (D5) stays untouched.

## Technical direction

The flattened map is the SAME world — not a schematic, not a top-down camera on a still-round planet:

- A shared **flatness morph (0→1)** applied to the planet and every surface element (sites, pipes, packets in flight, effects) — sphere → plane (split at the back seam, poles handled deliberately). One scene, one simulation state; the toggle animates the morph, so the "exact copy, just flattened" invariant holds by construction.
- Architecture lives in `scenes/levels/level_base.tscn` + shared view-mode plumbing so every level inherits it (structure folders/scenes accordingly per the user).
- HUD toggle button (planet ⇄ flat map) + sensible flat-mode camera framing (existing orbit_rig adapts; rotation/limb-marker behavior in flat mode specified in the spec step).
- **Transition animation (user ruling 2026-09-10, 16:3xZ):** "the animation of switching between globe view and flat map view can just be a zoom out. nothing complicated, but we need animation to transition smoothly." The transition = a smooth camera zoom-out carrying the flatten morph — no elaborate transition choreography. Smooth easing, interruptible/reversible (toggling mid-morph animates back cleanly). This REPLACES any fancier transition flourish; issue #25's morph-transition item shrinks to polish-only-if-needed.
- Ground before building: `scripts/world/flow_view.gd` + `scenes/flow_view.tscn` already exist — reuse/extend that view-mode pattern rather than inventing a parallel one.

## Models / verification (quota-hold regime)

- Build on **glm-5.3 @ max** (or k3 per current availability) — code + scene structure.
- Visual verification via the **vision skill** (user ruling: vision covers visuals; Astra is for 3D craft): captures of planet vs flattened for the same state — "exact copy, split and flattened" is the check.
- Any godot execution (suite runs, screenshot captures) is GATED on the user's pending bounded-run authorization — build + static checks + tests written first; if the user says "run", suite + captures proceed under that grant.
- If the morph's seam/pole/lighting craft needs deep 3D judgment beyond what lands cleanly, that polish goes to issue #25 (Astra, post-hold) — disclose, don't fake.

## Bounds

- No OpenAI usage. No Blender. Don't touch the hotfix lane (pS6) or the frozen Selva lane.
- pr_review=1, focused PR to main, no merge. Perkins round on glm-5.3 per the sanctioned hold regime.

## Dispatch parameters

- job_id: packet-plumber-3d-constellation-view
- repo: packet-plumber-3d · repo_root: /Users/moses/code/packet-plumber-3d · github_repo: solarity-services/Packet-Plumber-3D
- slug: constellation-view · base: main (post-#22 head)
- model: zai-coding-cn/glm-5.3 · thinking: max · pr_review: 1
- Skills: bmad-build (mandatory gate; ambiguous-short-config halt → job-local qualified-token binding per gemini-storyboard-internal-unblock-2026-09-10.md), gds-quick-dev for the game-implementation shape, vision-read for the screenshot checks (when execution is authorized).
