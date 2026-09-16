# Implement production L1 spawn awareness — GitHub #37

## Authority and outcome

**CURRENT CONTINUATION (2026-09-14):** user authorized fixing the confirmed PR42 warning set, with GLM5.3 where suitable. Read `/Users/moses/code/_bmad-output/briefings/pp3d-pr42-warning-fix-2026-09-14.md` FIRST for the existing-owner/existing-PR scope, fresh verification/review requirements and scoped model override. Initial-dispatch/fresh-worktree instructions below are historical setup, NOT an instruction to create a duplicate.

User selected planet-only; constellation is CANCELLED, not paused. After Gru proposed the behavior below, user said:

> let's see it in action.
> not a prototype. let's implement that in level 1.

**Implement the feature in normal playable Level 1 and deliver a verified PR + actual gameplay evidence + an isolated playable build.** No prototype-only scene, opt-in demo flag, mock UI, design-only result or pre-implementation option-selection gate. The original #37 future-only/no-option-approved/design-exploration/flat-view requirements are superseded by these explicit human messages. Update #37's current authority/title/acceptance, preserving original intake as historical. Issue: https://github.com/solarity-services/Packet-Plumber-3D/issues/37 . No duplicate issue.

Read `/Users/moses/code/docs/orchestration-playbook.md` Minion standing orders and `/Users/moses/code/docs/minion-field-notes.md`. Your canonical ledger row is **packet-plumber-3d-l1-spawn-awareness-37**; self-report THAT id, never self-create a shortened duplicate. Factory completion contract: `/Users/moses/code/_bmad-output/memory/result-oriented-routine-execution-autonomy-2026-09-12.md`. Implement, debug, verify and address review findings through usable delivery. Only genuinely critical decisions/out-of-mandate boundaries return to user; routine fixes/imports/retests and internal spec approval are owned execution, not user permission chores.

## Scope and accepted experience

Single goal: the player notices and can locate newly revealed buildings in **L1's existing tiny-planet game**, including buildings behind the sphere, without camera hijacking.

1. **Visible reveal:** retain the existing pop and add a restrained, legible local ripple/highlight in the game's palette. No giant beacon, fireworks, persistent strobing or added full-screen log panel.
2. **Hidden/far-side/off-screen reveal:** display a compact directional marker at the visible planet limb (or viewport boundary when the projected limb is outside the window), plus a small persistent **New buildings: N** control. Explicitly distinguish sphere occlusion from merely being outside the camera frustum. Projection must stay stable at the antipode/poles, across orbit and all zoom stops; overlapping markers group rather than pile up.
3. **Opt-in focus:** clicking a marker targets that building; clicking the count visits pending buildings in stable order. Smooth roll-free orbit, no surprise zoom-in; preserve the current zoom ladder position. Manual orbit/zoom/cancel takes control immediately. Focus must not fight another input owner or keep chasing after cancellation.
4. **Persistence:** queue/count survives a timer, the local ripple ending, camera motion and intervening gameplay. Acknowledge only by deliberate completed focus/inspection or explicit dismissal, not a fleeting on-screen glimpse or blindly on click. Interrupted focus must retain the unseen item. Multiple arrivals accumulate without losing identities; cycling must actually reach every pending building.
5. **Player control:** arrivals never steal the camera during drawing, selection, placement (including armed click-click placement), or manual orbit. An alert arriving mid-gesture queues normally. Alert controls must consume their own UI input and never draw a cable/install through the overlay; releasing a world drag on an alert must not activate a focus click. Retain existing cancellation/focus-loss behavior. Existing authored tutorial beats are not a license for the NEW awareness system to auto-orbit on spawn; preserve narrative/progression rather than silently reauthoring it.
6. **Actual L1 integration:** cover UCLA/SRI story reveals and UCSB/Utah GROW host reveals. One discovery item per newly revealed campus/building, not two duplicate alerts for its host/IMP pair or repeated `_process`/install synchronization. The player placing an IMP must not rediscover the already announced campus. Reset/restart/teardown clears UI, targets, signal connections and queues; no stale item in a new run/editor preview. No change to authored reveal timing, placement/layout, seed, traffic, command/replay semantics or win progression to make the feature easier to demonstrate.
7. **Visual quality:** unobtrusive in the existing HUD; remains discoverable against water/terrain and beside the current IMP/story/inventory panels. No overlaps or unreadable counters at narrow/standard/ultrawide viewport sizes. Use icon/shape plus text, not color alone. Works muted. The separate #41 sound-design job is NOT folded here; no audio downloads/paid assets/new soundtrack required.

## Code map / traps (verified on main 39d82d0632ca2b0b1b4bd190a089e0f5444e20aa)

- `scripts/levels/l1_arpanet.gd`: `_set_beat`, `_reveal_campus`, `_pop_site`, `_sync_installs`, `_build_ui`, placement polling. Sim stages nodes before they are visibly revealed; hook actual view reveal, not allocation/setup. GROW bare hosts call `_pop_site` directly, and `_revealed` tracks campus-cable/IMP installation state: using only `_reveal_campus` or `_revealed` will MISS real arrivals or duplicate them. Verify this in the clean tree.
- `scripts/input/orbit_camera.gd`: `frame_point` gives an existing target-azimuth/latitude basis; `orbit`, `zoom`, `snap`, no-roll/clamp/zoom-ladder contracts. Reuse sound mechanisms; do not transplant cancelled flat camera classes. Existing `frame_point` alone is NOT a completed interruptible focus/acknowledgment system.
- `scripts/input/input_router.gd`, `connect_controller.gd`: real physics/UI input routing and gesture ownership. Node press means DRAW, not an invented inspection mode. New cue UI must not break it.
- L1 placement is ALSO polled: `_pointer_over_dock()` currently protects the dock. Merely consuming `_unhandled_input` is insufficient to prevent installation THROUGH a new alert overlay. Test and preserve the complete interaction chain.
- `scripts/ui/hud.gd`, `scripts/world/node_site.gd`, `scripts/levels/level_manifest.gd`: follow existing rendering/theme/lifecycle; do not change manifest timing/layout.
- Tests: `tests/test_level_l1.gd`, `test_camera.gd`, `test_input.gd`, `test_view_interaction.gd`, `test_inventory_dock.gd`, `test_hud_lifecycle.gd`, `run_tests.gd`. Capture: `tools/l1_capture_runner.gd`, real main scene `scenes/levels/l1_arpanet.tscn`; existing correct entry `godot --path . -- --capture-l1` (default main scene, one user flag), NOT a runnerless alternate scene.

## Acceptance and evidence

Write the compact implementation spec with explicit Given/When/Then tests from this brief; no user midpoint spec gate.

- Given normal L1 play, when each authored reveal happens, then the visible local cue or occlusion-aware marker AND persistent discovery state appear through production code. Given a host/IMP pair or repeated sync, then exactly one campus discovery is queued.
- Given a far-side reveal, then the player can find and click its visible cue/count, the REAL camera orbits to the correct building at the existing zoom, and only completed focus acknowledges it. Arrange the witness by orbiting away before an AUTHORED L1 reveal, not altering geography/timing or inventing a fake spawn just for evidence.
- Given two queued reveals, then no event disappears by timeout; focusing/cycling handles both. Given focus interrupted by manual input, then input wins and the unvisited item remains pending.
- Given an active draw or drag/click-click placement, then a reveal does not change its camera/state or commit a graph/install action. A full press→motion→release onto/through new UI must not leak a world action or steal the pending gesture. Existing legal draw/install, invalid release, cancellation and focus-loss paths still work.
- Given restart/scene teardown/editor preview, then no stale alert, double callback, queued freed node or leaked visual remains. View-only actions leave simulation/replay state untouched.
- Prove meaningful failures: disabling reveal enqueue must fail a real-GROW test; disabling focus movement must fail the far-side target/ack test; removing the new overlay occlusion guard must fail a real-input test. Restore and re-run GREEN. No screenshot-background pixel count or direct-helper-only proof substituted for behavior.
- Run import, focused tests and full suite with the semantic `EXPECTED_CHECKS` count + completion flag + final `SUITE RESULT` guard. Exit 0 without a completed summary is NOT PASS. Preserve RED/diagnostic evidence; stop dependent stages, fix and bounded-retest. No vacuous checks or unexecuted tests represented as green.
- Deliver real moving gameplay evidence showing local reveal, hidden reveal→marker click→camera focus, two queued arrivals and user interruption/gesture safety. Plus an isolated normal L1 playable preview with exact start/controls/reproduce/exit instructions. No special flag needed for the FEATURE; deterministic capture tooling may have flags. Do not present fake/HUD-only HTML as in-game evidence.

## Boundaries / cleanup / execution

Fresh isolated worktree from **origin/main**, never the cancelled constellation tree. Live GitHub main was the sha above and no open PR at intake; re-resolve at dispatch. No constellation source/classes/toggle/assets/tests, hidden feature switch, dead-code archive or cherry-pick of unaudited experiment code. Archive remains OUTSIDE active game. Coordinate narrow cancellation canon/comment cleanup with Silas: if not already in its own PR, fold only the user-ruled stale promises/comment into this PR, explicitly historical content marked superseded. **Lavish not needed, PR directly** for that targeted doc/comment amendment; do not start a broad docs rewrite or revive flat-mode scope.

Only #37/L1 now. No other #34–41 features, later-level implementation, Odin modification, living-planet asset replacement, Resolve action, native Selva/H3 revival, or Wan interruption. User's concurrent PP3D/Wan use remains allowed; caveat performance under sharing, do not serialize on instinct.

Before native execution, declare adequate finite batches/timeouts/output and cleanup reserves under the standing factory mandate. Routine import/focused/full entries <=300s; allow a disclosed adequate capture window (up to900s as needed for world generation), `caffeinate -dimsu`, full log tee and exact-owned cleanup. A batch is not a user approval token: seal spent counters honestly and declare next bounded batch for ordinary remaining work; no quiet extensions/reset, no overrunning real user limits. Fresh worktree needs import remaps and `_bmad` bootstrap with Godot `.gdignore` facade as appropriate; do not mutate shared BMAD target or delete asset `.import` sidecars. Standalone preview, never alter/close user's editor. Mark USER LOOK ACTIVE at delivery; preserve viewed resources until user done.

## Model / skills / review

**Original implementation ran Astra/xhigh. CURRENT PR42 WARNING REMEDIATION overrides that pin:** parent/mechanical helpers and independent mechanical fix-audit round main plus every canonical lens use **`zai-coding-cn/glm-5.3` at `max`** under the dated amendment above. Actual native visual verification uses **`openai-codex/gpt-6-astra` at `xhigh`**, separately and truthfully disclosed; GLM cannot certify pixels. This is a scoped application of the user's conditional choice, not a global model change. Reuse the existing owner/session; verify successful model/thinking changes and delivered amendment. For any fresh launch clear inherited `PI_MODEL`, `PI_PROVIDER` and identity overrides, pin CLI values and verify actual metadata plus canonical handover, never footer-only provenance.

Implementation: **bmad-build**, generated for THIS project/worktree (renderer exists at the PP3D main checkout `_bmad/scripts/render_skill.py`; bootstrap safely and follow skill exactly). Execute planning/implementation/internal review steps; normal internal approval checkpoints pre-approved, no prototype interpretation of a generic workflow heading. Visual evidence: native Astra image inspection and **lavish** for reviewing actual captures if helpful, not a substitute for playable Godot. Independent review: **code-review** full canonical seven lenses (blind, edge, acceptance, security, architecture, codebase, tests), read skill first, prompts verbatim, blind diff-only and others read-only. Canonical spec is the new #37 production spec, not frozen constellation sources. Review exact stable PR sha; loop until blockers addressed/APPROVED, preserve truthful findings, never merge.

## Completion / dispatch

Commit, push, `gh pr create --base main`; include decisions/rationale, honest suite and visual results, screenshots/clip paths and play instructions. Run `ledger pr packet-plumber-3d-l1-spawn-awareness-37 <URL>` AND set in-review. On completion deliver PR + playable/evidence location through Silas to Gru. Self-notify checklist with actual `herdr notification show` result pasted (`shown:true` required), never merely claim. No final 'source done' followed by idle while verification remains.

```yaml
repo: packet-plumber-3d
repo_root: /Users/moses/code/packet-plumber-3d
slug: l1-spawn-awareness-37
base: main
model: zai-coding-cn/glm-5.3
thinking: max
visual_verification_model: openai-codex/gpt-6-astra
visual_verification_thinking: xhigh
github_issue: 37
pr_review: 1
job_id: packet-plumber-3d-l1-spawn-awareness-37
```

Silas owns registration, clean main-based dispatch, issue authority update, provenance/delivery checks and unused-minion cull. One implementation owner, no duplicate fleet. Close cancelled/unused minions after preserving their records, but do not make unrelated archival housekeeping a blocker on this accepted production feature.
