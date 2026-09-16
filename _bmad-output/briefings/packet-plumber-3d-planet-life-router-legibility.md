# PP3D — biome wildlife, ambient animation, router legibility

## LATEST OPERATIONAL CORRECTION — scheduling expiry is not a consumed native run

Read `/Users/moses/code/_bmad-output/briefings/pp3d-ab-fresh-scheduling-correction-2026-09-09.md`: first A/B host context refused a stale Silas scheduling receipt before claim/Popen, native budget0/2. Gru explicitly approves a NEW linked scheduling context with fresh actual ownership/availability facts/receipt and immediate preflight→launch, keeping180s/technicalTTL/90s/512MiB limits unchanged. Preserve failed reports/journals, no native retry/code change/waiver or new user A/E. This applies ONLY to still-unconsumed A/B diagnostics; original3-stage retest failure and moth USER STOP remain controlling.

## LATEST DELEGATED DIAGNOSTIC AUTHORITY — editor-only A/B (2026-09-09)

Completed cleanup retest remains TERMINAL/FAILED final editor inspection; family/dolphin scoped PASS and editor automated PASS remain separately preserved. NEW explicit Gru-delegated approval at `/Users/moses/code/_bmad-output/briefings/pp3d-editor-shutdown-ab-diagnostic-2026-09-09.md` permits ONLY two matched isolated BEFORE/AFTER native editor quit diagnostics, same pMY/session,90s/512MiB each, no retries/instrumentation/repair/capture/waiver. This is not revival of the consumed capture grant below. Same warning in both proves pre-existence, NOT engine-only/harmlessness. Read the complete new diagnostic brief; no new user A/E. Moth latest USER STOP and ongoing independent storyboard review remain unaffected.

## LATEST USER GRANT — shutdown cleanup repair + one fresh smoke pass (2026-09-09)

User explicitly answered **“yup.”** to the focused cleanup diagnosis/fix plus ONE bounded family → dolphin → editor retest proposal. This supersedes this job's terminal-failure repair/retest hold ONLY. Controlling new grant: `/Users/moses/code/_bmad-output/briefings/pp3d-shutdown-cleanup-repair-retest-2026-09-09.md` — read completely before resuming SAME parent/session/worktree. Preserve old failed receipts/cancellation, dirty current features and user instances. No broad suppression/engine changes/animal redesign; source-bound retest uses120/120/90s external watchdogs and512MiB live caps, cancels on first failure, no retry. No new routine user A/E is owed. No PR/push/merge/Perkins or whole-world acceptance. **Selva moth hard stop, ended storyboard/player/static-server read-only and SOMA park remain unchanged**; historical resume language below is not authority for those lanes.

## USER-DELEGATED ROUTINE PLAN APPROVALS (2026-09-08)

User: “handle routine plan approvals for these two jobs”. For this current PP3D amendment, route routine scope/spec/planning checkpoints to **Gru through Silas**, not back to the user. Independent review/testing remains mandatory; scope changes and final visual/play acceptance remain the user's. This is not global delegation or new remote/destructive authority.

Gru read the complete companions/dolphins draft and **A — APPROVED** it at SHA256 `ee9fb7f0bb541fbc4b05c89c8c7d3c9822cd9bf47e1159779276ca6ff60ee3a5`. KEEP BOTH scope is already settled. Proceed past the compact-spec checkpoint into implementation; update administrative spec status/changelog, do not re-ask A/E. Substantive in-scope plan revisions return to Gru; out-of-scope changes go to the user. Durable approval contract: `/Users/moses/code/_bmad-output/implementation-artifacts/pp3d-selva-delegated-plan-approvals-2026-09-08.md`. All user-window/ownership/quality/review and separate remote/merge constraints below remain intact.

## USER ADDITIONS — companions, polar-bear cub and breaching dolphins (2026-09-08)

Verbatim:
> look good. a few things to add. the seal should not be lonely, the polar bear should have another company in their regions, and may one should have a cub. then we should have dolphins in the water, jumping in and out of the water with splashes.

The user accepts the current boat/wake LOOK and asks for these additions. Preserve the boat fixes at `d2ffebbe05c603419516b85fe13e5f45295eca1f`; no repeat boat-style question unless a new regression appears. This is NOT push/PR/merge authorization, nor a blanket E2/L1 gameplay verdict. Continue the SAME existing job/worktree, no duplicate dispatch.

### Requested scene behavior
- **Seals:** a visibly companionable pair in the same suitable icy region/clearing—not two distant animals on opposite sides of the globe or a population constant with only one surviving placement. Use modest posture/phase variation; no new behavioral simulation.
- **Polar bears:** a small family in its own suitable icy region: TWO adults plus ONE recognizably juvenile cub as the concrete interpretation offered by Gru. Numbers beyond the requested companion/cub are implementation defaults, not invented verbatim user language. The cub stays near the family, with sensible juvenile proportions and calibrated contact/footprint; avoid a scale-only hack that breaks the articulated foot placement. Group members must not overlap, march as one rigid object or wander outside their habitat. Keep the existing friendly low-poly style and other animal species stable.
- **Dolphins:** start with a small pair, original recognizable dolphin silhouettes (snout, dorsal fin, pectoral fins, horizontal tail flukes), subordinate to gameplay landmarks. Smooth swim→emerge→airborne arc→re-entry→submerged intervals, pitched along travel, with staggered phases rather than synchronized jumping props. Generate restrained splashes/ripples at the ACTUAL water-surface crossings, especially re-entry, which expand/fade at their historical water location. No constant foam fountain, visible teleport, frozen airborne dolphin, shark-shaped substitute or arbitrary emitter offset. Scope is ambient life, not a marine-physics/shipping simulator.

### Grounded implementation / correctness
- Gru read `ambient_life.gd`: `PER_SPECIES=2` already attempts two of every species, but independent `AmbientRoute.build` can reject candidates and places/reserves individually. Therefore **verify actual realized proximity/population before assuming a count increase fixes loneliness**. Group-aware safe placement/spacing may be needed; do not simply raise PER_SPECIES globally. Current MAX_ANIMALS10 and existing resource caps need deliberate bounded updates/pins if the added cub changes totals.
- Deliver visible seal pair and bear family in normal default and L1 worlds. Inspect actual native entities/captures, not requested-count metadata. For pathological constrained/custom seeds retain safe bounded omission/fallback and disclose it; do not silently ship singleton default/L1 groups as success. If requested family cannot fit, report the actual geometric constraint rather than violating containment or expanding terrain silently.
- Full articulated footprints and complete swept group routes stay in their ice habitats; preserve planted contact and pairwise spacing. Cubs must not clip adults or skate as a detached scaled rig. Other species' gait/path/look and approved ivory75/pulse/click behavior remain unchanged.
- Dolphins' full submerged/airborne trajectory and landing/splash footprint must stay over navigable water, clear of shores/islets/boats/lighthouse/other actors. Respect actual faceted Water geometry/local normals, water occlusion and composed mesh orientation/pivot/scale. Preserve the fixed boat stern emitter and noncircular patrol contracts.
- Everything remains view-only and deterministic from explicit controlled time/seed: no simulation RNG/state/replay dependency, accumulated random animation, wall-clock shader TIME or history-dependent particles. Reconstruct splash lifetimes analytically/through bounded reusable slots; pause freezes motion/effects and random seek/rebuild agrees with continuous evaluation. No unbounded per-frame spawn/search or uncapped memory/triangles.

### Proof and delivery
1. Baseline is d2ffebb, not earlier549/173 receipts as proof of NEW features. Add direct realized-group/proximity/age-scale/contact tests; missing companion/cub must fail the representative-world requirement. Verify whole swept habitat/population spacing independently.
2. Test actual dolphin emergence, fully airborne and fully submerged phases, oriented entry/exit, splash location at actual crossing, timing/fade/expiry, bounded pool and no dry-land hits. Independent negative controls must fail for a removed companion/cub, wrong landing/splash offset, disabled jump or frozen/never-expiring splash. Preserve harness EXPECTED_CHECKS/completion/final-line fail-closed behavior, tiny-water regression and replay purity.
3. Fresh native normal frames and moving clips: visible family groups and COMPLETE representative dolphin jump/landing/splash cycles from useful fixed close and normal orbit/zoom views. Do not claim all-frame visual inspection from a few stills. Match source hashes/reviewed snapshot and disclose performance contention/cost honestly.
4. Use the existing bmad-build workflow for bounded implementation, independent review, all required verification and local commit. Keep changes in same branch; no automatic push/PR/merge while that question is unanswered. Full actual-PR-SHA seven-lens Perkins and renewed whole-world play/look remain separate.
5. On delivery, prepare a genuinely runnable fresh-imported normal preview. Last raw-worktree launch failed to register AmbientWaterRoute; use an isolated exact-commit copy/fresh cache and explicit `res://scenes/main.tscn` for the default planet, or explicit L1 only when requested. Window-exists is NOT readiness: verify no script errors and actual populated scene. Do not reopen/reload the user's existing preview automatically.

### Coordination / skills
Existing parent w85:pMY is the writer; retained w85:pN2 supports read-only unless parent explicitly transfers sole-write duty. Use bmad-build (load/render skill in the actual worktree), context7-docs for API details, and native Astra vision. Parent/helpers/reviewers ALL `openai-codex/gpt-6-astra` / **xhigh**, verified. Preserve the user's Godot instance and USER PLAY/LOOK HOLD; no sweep/restart while viewing.

The user ALSO explicitly resumed Selva in a SEPARATE new collision-fix brief. That supersedes old blanket Selva-park references below, not PP3D's isolation rule: never mutate Selva's shared Blender scene or revive its old asset scope. Prefer existing Godot-native fauna/mesh patterns for dolphins. If an isolated Blender asset worker is genuinely needed, coordinate through Silas without taking the shared interactive owner. Coordinate heavy GPU captures/renders; no sustained-FPS claims under shared load, no blanket blocking of either lane. Typography stays deferred.

## USER PLAY FEEDBACK — boat routes and wake alignment (2026-09-08)

Verbatim:
> the boats are moving in a circle. and the ripples are at the wrong location. slightly off center from what i can see

This reopens bounded boat/wake work IN THE EXISTING job/branch/session; no new job or replacement minion. Interpret as an iteration request, NOT final play/look acceptance or push/PR/merge authorization. Current stable local pre-amendment commit: `f0fd52989d2777bd00aec0317a430be3d505c25b` (resolve before work). Existing source/evidence remains baseline; preserve it before new captures. Router ivory75, animal scope and typography deferral stay untouched. Selva is hard-parked and must not be resumed for this.

### Intake evidence — Gru inspected source and native images inline on Astra
- `scripts/world/ambient_route.gd` explicitly implements a **seeded closed small-circle** (`axis*cos(angle) + cross_axis*sin(angle)`), including water routes. This confirms circularity is implemented, not merely a guessed camera artifact. Its six-beat/rest timing is shared with fauna; do NOT globally redesign animal routes/gaits to fix the boat complaint.
- Existing `.scratch/planet-life/parent-audit/review-fixes-20260907-235926.wWCdRw/motion/default-boat-0120.png` and `motion-samples/boat-loop-samples.jpg` show a trail visibly detached to the side of the hull in the sampled view. This corroborates the user's visual concern, NOT a proven exact origin/axis bug. These are prior captured output at the pre-amendment state, not a fresh capture of the user's live window.
- `scripts/world/ambient_water.gd:evaluate/_wake_tracks` emits from `route.sample(emitted)` with a generic `hull * 0.55` offset; the holder adds its own bob/roll and the authored mesh has a separate orientation/scale transform (`props.gd` says authored bow+X -> ambient-Z). These are investigation leads. Verify actual mesh bow/stern, waterline, visual pivot/centre and the complete transform chain before choosing the fix; do not blindly flip a sign or shift an arbitrary constant until this particular camera looks right.

### Bounded correction and acceptance
1. Replace the water-only small-circle merry-go-round with readable natural **directional travel and gentle turns** within certified water space. A finite patrol may eventually return, but must not just make the same obvious small circle larger, jitter it, teleport/reset, pivot in place or disguise the loop with the camera. Choose a small deterministic water-route solution appropriate to the existing architecture; no general pathfinding/new shipping simulation or animal movement overhaul.
2. Anchor NEW wake/ripple emission to the boat's **actual stern/waterline centreline at emission time**, accounting for final mesh basis/orientation/scale/pivot and the local water surface. The trail must read as coming from the hull and trailing travel, not appearing beside it. V-shaped wake arms may widen; old wake segments should remain at their historical water locations and fade/spread—not stick rigidly to the moving boat. Define and verify any physically motivated separation rather than using an arbitrary visual offset. Prevent a powered-looking forward wake while a boat is not moving.
3. Preserve water-only containment of the **whole transformed hull, full swept route including turns/seams, and all wake geometry throughout lifetime**. The earlier tiny-water radius10 regression must remain fixed. No endpoint-only or centre-only substitute, no routing through land/islets/lighthouse/other boats, no NaNs/surface snapping/capsize. A safe supported stationary fallback is preferable to invalid motion when no navigable corridor fits. Keep view-only determinism, isolated seed/time, random seek/rebuild equivalence, pause behavior and bounded pool/runtime cost.
4. Reproduce the before state, then verify the actual corrected native output at at least two boat headings/views and the relevant default/L1 worlds. Inspect a COMPLETE representative trajectory cycle/return seam and wake lifetime, not just the old12 sampled stills. Include moving fixed-camera close views plus normal orbit/zoom; evidence should show bow/tangent alignment, newest-emission attachment and older trail behavior together. Named clips/annotated geometry anchors are evidence; model praise is not acceptance. If no boat exists in a constrained world, disclose it rather than fake coverage.
5. Add meaningful geometric/behavior regressions and independent RED→GREEN mutation legs: offset/rotate the real emitter incorrectly must fail; restore circular water-path behavior must fail a targeted non-vacuous path-shape/heading test; full hull/wake swept containment and bounded deterministic evaluation still pass. Test the actual implementation/output, not metadata that only says noncircular. Run relevant native/full suite/replay checks and independent bounded-diff review via the existing bmad-build workflow. Previous501/125 greens do NOT prove these newly requested changes.
6. Return new local commit + concise diagnosis/evidence showing what changed and what remained fixed. No automatic remote push/PR while existing authorization question is unanswered. Full seven-lens Perkins remains required after an authorized PR exists at its actual SHA; renewed user play/look acceptance remains separate. No new font/router-choice/Lavish approval ceremony.

### Session / skills / safety
- Existing parent w85:pMY and retained implementation helper w85:pN2 (re-resolve) own this fold; use bmad-build for bounded implementation/review/verification and context7-docs for any API-specific uncertainty. All 3D work/helpers/vision remain `openai-codex/gpt-6-astra`, **xhigh**, verified; no silent model fallback or new mega-fleet.
- User is actively inspecting the game: Silas records a USER PLAY/LOOK HOLD against destructive cleanup. Preserve the worktree, parent/helper and user's running Godot instance; do not close/restart/reload their app or mutate the shared editor scene to reproduce. Author the bounded patch and use isolated native processes/evidence as needed; let the user choose when to reload to try it. No Blender work/restart, no Selva revival, no typography fold.

## User request / scope
Enhance the existing Packet Plumber 3D planet with animals inspired by three user screenshots. Animals move naturally within defined restricted habitat paths (explicit example: polar bears stay in the ice region). Animate existing boats with water ripple/wake effects and rotate the lighthouse light. Improve router contrast so devices stand out while fitting the current palette; compare half the current size against 25% smaller.

This is ONE new PP3D enhancement job with two coordinated workstreams, not two duplicate dispatches from the repeated user message. It is completely separate from Selva Eléctrica / youtube-channel. The user's subsequent premium YouTube quality amendment belongs to Selva, NOT a request to make this low-poly game photorealistic. Preserve PP3D's rounded/faceted little-planet style and readable gameplay.

## USER SIZE DECISION — resolved
After choosing ivory as the colour direction in Lavish and seeing the normal 100%/75%/50% evidence, the user was asked: "Shall we use 75%—25% smaller than the original?" User replied **"75 is fine"**.

Selected shipping router visual default: **ivory palette, 0.75 linear scale relative to the original baseline**, preserving tier-relative dimensions. This is 25% smaller, NOT 75% smaller or 25%-of-current. The router palette/size decision gate is satisfied; do not ask again or hold the PR for it. Update the actual runtime defaults and decision record, then re-run relevant tests/evidence at the chosen setting. Prior 100/75/50 options remain diagnostic comparison history, not unresolved choices.

This selection is NOT final whole-planet play/look acceptance, a waiver of code review/Perkins, or merge authorization. Optional species-motion polish remains non-gating.

## User amendment — no purple router look; separate diagnostic passes
User clarified that the minion to inform about the completed Blender MCP startup tooling is the ROUTER/PP3D minion (not Selva), and said:
> wirking on the router. why the routers glow purple...i saw that in the tests. purple is ugly.

User aesthetic preference: no purple glow as the intended router look. After Gru explained and verified the diagnostic ID mask, user replied **"i see that's fine then"**. The purple-test question is RESOLVED: diagnostic magenta is accepted, not a requested rework. The later decision above locks ivory/75%; temporary measurement masks remain instrumentation only.

Gru checked actual worktree code and paired PNGs: tools/planet_life_capture.gd `_routers()` temporarily replaces router body surfaces with an UNSHADED pure-magenta Color(1,0,1) ID material, captures `*-mask.png`, restores prior overrides, and uses identified pixels for contrast metrics. The paired normal `default-n21-edge-z1-contrast-75.png` is slate, while its `-mask.png` has the bright magenta body. `_palettes()` already describes clean visible exploration with no debug pass. Current RouterStyle candidates have no purple option. The visible test-mask pass is the evidenced explanation; do not misreport it as a chosen glow/emission design.

Leave the diagnostic tests intact; no new task to hide/suppress/rebuild them is authorized or needed following the user's acceptance. Use normal non-mask frames for actual palette/size choices and distinguish diagnostic artifacts from proposals. Existing correctness still requires temporary material overrides to restore rather than leak into runtime/final frames. If clean runtime actually shows purple, investigate that separate failure. No global palette rewrite or invented selected default.

## Blender startup tooling handoff (informational)
Completed startup lifecycle source/docs/tests are preserved in `/Users/moses/.herdr/worktrees/code/blender-mcp-reliable-startup`, commit adaffdb. Successful live Selva restart/identity proof has been reported; this is not authorization for a NEW restart or to take Selva's shared scene. Consult its actual documented managed enable/start/stop/status path for future Blender use; honor deliberate opt-out and listener-free background workers. Coordinate isolation/safe ownership transfer with Silas as before. No need to pause game/router work merely to acknowledge this informational handoff.

## Reference intake and evidence
Files preserved outside all repos at `/Users/moses/code/_local-refs/pp3d-ambient-life-2026-09-07/` (README records source/rights):
- `Screenshot 2026-09-07 at 18.36.35.png`: arctic, polar bears and seals on snow/ice floes.
- `Screenshot 2026-09-07 at 18.36.14.png`: farm/meadow, sheep in a fenced paddock.
- `Screenshot 2026-09-07 at 18.35.52.png`: forest, deer and fox by trees/paths/stream.

Gru inspected all three inline. Study them directly on Astra and create an evidence-graded element table before choosing designs: species silhouette/proportion, habitat, density, motion proposal and actual implementation counterpart. STILL screenshots do not prove movement; natural-motion requirements come from the user's words, not an invented reference-video analysis. Reference game/creator/license unknown. Use as inspiration only: no tracing/extracting or copying reference models, UI, buildings, textures or image pixels into the repository. Cite paths; comparison reference images stay local via loopback serving, not committed derivatives.

The router complaint is user evidence. Main's code confirms green edge routers and terrain with nearby hues, but committed captures may be stale relative to the last fixes. Capture the ACTUAL current runtime/head before diagnosing, measuring, or showing before/after. Do not present an old committed screenshot as a fresh test.

## Current base / key pointers
- Repo `/Users/moses/code/packet-plumber-3d`, remote `solarity-services/Packet-Plumber-3D`, base `main` (NOT the 2D repo's v2).
- Last inspected local main: `0818afc2ca77ec5ef514d555f7c954fd567539ef`, merged PR #17; resolve current origin/main at dispatch. Base clean when inspected. R7 receipt: 374 checks PASS, replay byte-identical, limb CIRCLE, 32-frame sweep clean; re-run rather than assuming.
- Read `README.md`, `LOOK-PARITY.md`, `assets/README.md`, attribution files, current GDD/epics, `_bmad-output/implementation-artifacts/spec-alive-planet.md`, `spec-router-family.md`, `spec-l1-look-parity.md`, and `deferred-work.md`.
- `scripts/world/props.gd`: seeded stage/keep-outs/150k triangle discipline, existing pp_boat instances, `_stage_lighthouse` with seated fixed tower and emissive lamp + OmniLight3D. Current boats and lamp are static.
- `scripts/world/world_seed.gd`: biome_at, snow_at, terrain/rivers/islets, seeded salts and palette. Existing map includes polar snow overlays beyond biome-2; match the VISIBLE valid ice/snow surface and safe land support, not a naive single biome-number assumption.
- `scripts/main.gd`: shared runtime/editor staging, view processing and regeneration.
- `scripts/world/node_site.gd`: router GLBs carry tier materials (no device tint at stage), ROUTER_DIMS edge=1.20 / hub=1.60 / core=2.00, scale normalization, collision and labels. pulse_egress() temporarily scales Visual to 1.14 then restores ONE: a new visual size adjustment must NOT be undone by the next pulse.
- `assets/junctions/router-round-{edge,hub,core}.glb`; in/out arrow grammar and round tier family must survive.
- `tests/run_tests.gd`, `test_alive_planet.gd`, `test_art_staging.gd`, `test_world.gd`, `test_view_purity.gd`, `test_view_interaction.gd`, `test_editor_preview.gd`; capture/replay tools and `tools/verify_limb_circle.py`.
- Read PR #17's r7 advisories W1-W6 and deferred docs; fold only items directly on surfaces touched here and report routing for the rest. Do not silently expand into unrelated simulation/export work.

## Workstream A — animals and ambient life

### User motion-polish note — OPTIONAL, not a new gate
User feedback:
> btw. inform the minion working on the animation, that the animals should have as close to their natural movement as possible. they all walk the same way.
User immediately qualified the priority:
> not a big deal, but would be nice to have.

Treat improved species-specific naturalness as NICE-TO-HAVE polish, not a new blocker/release gate or reason to delay router choices/PR readiness. The user's observation is that current creatures read as the same walk. Gru read `fauna_rig.gd`: it shares the distance/stride/contact loop across species with some species branches; do not claim no differentiation exists, but evaluate whether the visible differences are meaningful.

If modest in scope, improve characteristic movement rather than only varying speed/phase: a grounded heavy bear; distinct longer-limbed deer, compact sheep and lighter alert fox posture/stride/weight transfer; seals moving through body/fore-flipper action instead of reading as four-legged walkers. Preserve planted contacts, smooth turns/pauses, existing habitat/path constraints and presentation-only determinism. Shared implementation is fine; visually identical results are the concern. No large rig/anatomy overhaul, paid assets, mandatory animal-animation research lane or new approval ceremony.

Reuse existing motion clips to show useful improvements when convenient; no extra side-by-side clip gate required. If meaningful realism would substantially expand this pass, record a concrete follow-up in the owning deferred-work/issue route and report it rather than silently stretching the job or treating this as mandatory. Existing safety/correctness contracts (habitat containment, no sim effects, stable valid transforms) still stand.

### Animals
- Add a small curated set of recognizable original/appropriately licensed stylized animals corresponding to the references: polar bears and seals in suitable ice/snow habitats, sheep in safe temperate meadow/farm-like pockets, deer and fox in forest pockets. Do not build the reference's farms/cabins/characters/UI as extra scope. Preserve the reference's charm through silhouette/proportion and polished simple motion, not featureless substitute boxes.
- Build view-only bounded route/habitat definitions with natural walk/amble, short pauses/look/graze/rest beats and smoothly eased heading changes. Species-specific gait/body/head/limb motion should support travel; translating a frozen model or sliding feet is not sufficient. Desynchronize creatures in controlled, seed-derived ways; avoid synchronized parade loops or frantic random jitter.
- Keep every creature's WHOLE footprint, not only spawn/waypoints, inside permitted support/habitat. Check swept route segments and intermediate points with conservative clearance; splines can overshoot valid endpoints. Polar bears must never wander into green/desert/ocean. Seals stay on supported ice unless a separately approved swimming behavior exists (not required here). Sheep stay in their bounded grazing patch; no fence needed unless actually authored. Forest animals stay on safe forest paths.
- Seat to the actual curved terrain and face the route tangent using the local surface normal. Feet must not float, penetrate terrain or tunnel through terrain between waypoints. Avoid buildings, gameplay node keep-outs, rocks/trees, rivers/coasts and other blockers. Include loop closure/turnaround continuity; no teleport seam or instant 180° flip.
- Handle tiny/disconnected/no-valid habitats, empty routes, degenerate tangents and missing models safely with bounded generation effort. A stationary fallback can be graceful for a particular invalid habitat but cannot make every positive-case movement test vacuously pass. Include positive population/motion assertions on representative seeded and L1 worlds.

### Boats and water
- Reuse the existing boats; follow authored/seeded water-only bounded paths with gentle tangent-oriented heading, bob and roll. Validate the hull footprint and swept motion against actual water, coastline, islets and shoreline keep-outs. No boat traverses land or drives through the lighthouse.
- Add subtle water-surface wakes/ripples that follow movement, expand/fade and cleanly expire; restrained idle ripples are acceptable during rests. The effect must conform to the local curved ocean surface, remain at the hull/water contact, avoid land and not z-fight or become a huge flat plane slicing the globe.
- No full fluid simulation. Use a bounded low-cost effect budget, stable scene lifecycle and testable effect lifetime. Visual treatment must fit the turquoise water without stealing emphasis from packets/links.

### Lighthouse
- Rotate a VISIBLE directional lamp/beam sweep about the lighthouse's LOCAL UP / radial normal. Rotating an omni-light alone changes no illumination and does NOT meet the request.
- Keep tower/islet/foundation stationary and maintain the existing pad fit, top-mounted lamp scale and warm palette. No rotating entire tower, detached lamp, world-Y orbit or light cutting wildly through the planet. Subtle beam/spot evidence must show actual swept heading/light footprint at distinct times under a fixed camera.

## Workstream B — router contrast and size
- Measure/render the actual staged edge/hub/core materials, not just an unused COL_ROUTER constant. Improve base/body/rim/arrow/value separation against grass and across cold/sand/water-adjacent backgrounds and sun/shade while staying in the existing palette family. A restrained slate/cream/warm-accent direction is a candidate, not mandated final colors.
- Preserve round-device identity, tier size/detail ladder, incoming/outgoing arrow readability, existing material attribution and gameplay state semantics. Do not repurpose crisis red or make idle routers mimic active alerts/packet colors. Avoid neon outlines/strong bloom as the only way to see the device.
- Capture fixed seed/camera/light/times across (a) original baseline, (b) improved contrast at original size, and (c) improved contrast at 75% and 50% linear size. Include globe, district and street close views, representative tiers/biomes and a grayscale/value separation check. Report measured visual bounds and body-vs-immediate-background separation; do not invent accessibility thresholds or claim WCAG text criteria validate 3D objects.
- Visual size changes ONLY unless a coupled adjustment is necessary and justified. Keep the useful click/drag target rather than automatically halving it; recheck neighboring picks, empty-space orbit, front/back globe occlusion, link attachment points, labels and hover/selection affordances. Preserve placement/sim positions and tier selection.
- Verify egress/pulse animation returns to the SELECTED reduced size, not the original scale; no shared-material mutation that changes other assets unexpectedly. Retain base seating and proper labels/port alignment after scaling.
- The user choice on actual in-game size/contrast evidence is now IVORY / 75%, per the decision above. Reflect it in runtime defaults, tests, documentation and fresh normal captures; do not reopen the ended Lavish session or keep waiting for another size answer. Final play/look acceptance remains separate.

## Integration / invariants
- Ambient animation is presentation ONLY: no changes to SimCore, topology, route costs/capacity, node count, demand, serialization or command semantics. Own view RNG/clock; never consume simulation randomness or feed motion back into sim inputs. Prove replay/state hash unchanged with ambience on/off and at different frame schedules.
- Deterministic seeded population/routes and a controllable view time for captures, seeking and tests. Match existing pause/editor conventions; do not create a new settings system. Captures must freeze/evaluate ambient time explicitly, not flake with wall-clock shader TIME. Preview regeneration/reload must not duplicate animals, effect pools, signals or processing loops.
- Preserve perfect sphere/relief, terrain/river/islet geometry, tree populations and established look controls. No global palette/light/camera rewrite to hide router contrast or make wildlife look better.
- Respect existing geometry/effect budgets and measure frame cost before/after under comparable conditions; disclose machine contention. No blanket per-frame global path search or unbounded spawning. Culling/detail reduction is acceptable only when it preserves visible behavior and determinism at a given controlled time.
- Asset builds must be reproducible/documented and import correctly in Godot; check transforms, bounds, animation tracks and licenses. No Blender-only demo passed off as an integrated game feature.

## Verification and delivery
- Establish current-head green baseline. Add meaningful contracts for positive moving population, route/footprint containment, slope/surface seating, seam continuity, route fallback, deterministic view evaluation, wake lifetime/budget, true lighthouse sweep, router bounds/materials/pulse restoration/picking, and regeneration cleanup.
- Use representative default + L1 + multi-seed + edge-case coverage; sample interior curve segments and all animation phases. Do not merely assert endpoints or a computed helper that the runtime never uses.
- Mutation legs must show key gates fail: remove containment or introduce an out-of-region segment, freeze animal/boat progression, break wake decay, rotate only an omni/whole tower or freeze beam, restore old router size/material/pulse reset, abort a test file. Restore clean and re-run GREEN. Tie observed movement to rendered objects, not only time counters.
- Preserve the harness's per-file EXPECTED_CHECKS/run-count + completion flag + final-line contract. Printed check counts must match; an aborted coroutine/shortfall is FAIL. New tests must register in the actual runner. All important extracted constants get value pins; grep claimed fixes in the tree before reporting.
- Run full suite, headless import, default + L1 replay byte identity, existing limb verification, and new fixed-time captures. Independent bmad-build review and full Perkins required for this gameplay-adjacent/render code lane.
- Evidence includes actual in-game frames/short motion clips: arctic constrained animals; forest/meadow activity; moving boat + fading wake; lighthouse sweep; matched router options; orbit views checking clutter and network readability. No still-only “natural motion verified” claim. Inspect images inline on Astra and independently measure the claims.
- Update LOOK-PARITY/asset/animation control docs and a focused spec/decision log to match actual shipped behavior and chosen router scale. Docs support the code PR; no separate large GDD replan. This user ruling supersedes older green-router/size specifics only where explicitly changed; retain round family and untouched lore/era decisions.
- Final user play/look gate: give exact launch/click steps and camera/locations to inspect, and keep their worktree/pane intact while the user is viewing it. Final visual acceptance is the user's, not solely a model's self-review. No automatic merge.

## Tooling / concurrency / scope guards
- Godot is the runtime/evidence tool; use installed Godot MCP and current docs as needed.
- Any Blender work uses DIRECT Blender MCP (user ruling; no Higgsfield plugin/auth repair). Selva currently owns the shared Blender session/reservation. Coordinate through Silas: use a separately isolated Blender instance/endpoint if supported, or schedule an explicit safe handoff/short lease after Selva acknowledges saving. NEVER reset/switch/mutate Selva's scene, close its helpers, or steal its reservation. Code/route/test work may proceed while asset access is arranged.
- No paid downloads/generations, publishing or unrelated queue changes. Preserve other jobs/checkouts. Existing reference pixels never enter repo/PR; original in-game captures may.

## Skills policy
- bmad-build: scoped implementation, compact spec, verification and step-04 independent review.
- lavish: visual comparison and router choice; actual in-game evidence, matching playbooks (comparison/input). Clarification/choice halts are intentional.
- code-review: full Perkins set for round mains/helpers, canonical lens briefs and output contracts, no subset.
- Native Astra vision for all 3D/capture checks; use current Godot/Blender docs for version-specific APIs.

## Model policy
Minion, 3D art/animation/helpers, visual verification AND Perkins 3D round/lenses: `openai-codex/gpt-6-astra`, xhigh. This is the user's ALL-3D override, not Sol generic-helper routing. Pin full provider/model and thinking at EVERY launch; clear inherited overrides and verify session modelId/effective thinking. Missing/unavailable model -> escalate, no silent legacy fallback.

## Dispatch parameters
repo: packet-plumber-3d
repo_root: /Users/moses/code/packet-plumber-3d
slug: planet-life-router-legibility
job_id: packet-plumber-3d-planet-life-router-legibility
base: main
model: openai-codex/gpt-6-astra
thinking: xhigh
pr_review: 1
worktree: isolated from fresh origin/main (last inspected 0818afc)
github_issue: 0
coordination: Selva exclusive Blender reservation; arrange isolation/lease, never mutate its scene
visual_gate: router choice RESOLVED ivory/75%; finish verification/review then final motion/look proof and user-play gate (no merge authorization)
