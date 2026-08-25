--- YOUR LENS (source tag: architecture) ---

Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

Round-specific architecture invariants (from the project context + round briefing — verify, do not assume):

- ODN-1 (core/ is pure — vendor:raylib only in app/; the sim never sees the camera). The pullback's SEED classification is DERIVED on the view side (rnd.camera_spawn_is_seed reads topology+catalog, mutates nothing) — verify no core/ file changed and no new core dependency flows from this diff.
- ODN-12 (the intent layer: device event → map → intent → executor → app effect hook). The new chain is Mouse_Wheel → Zoom intent → exec → on_zoom/effect_zoom; verify the layering holds: policy (NOC-panel hit, modal block, clamps) lives in the app effect, the mapping carries raw data only, the pure math lives in app/render/camera.odin (no App, no View, no raylib state).
- ODN-13 (no globals — everything off App): the pullback state (auto_pullback/pullback) lives on App, NOT the View, NOT package globals — verify.
- The "one consumer" rule for the wheel: effect_zoom owns the NOC-panel-vs-zoom policy; the OLD unconditional wheel read in the render block is deleted — verify nothing else reads GetMouseWheelMove in the app path anymore.
- The §10.4 no-transcendentals rule on the rasterized path: camera_zoom_step uses repeated multiplication (no pow); CAMERA_PULLBACK_EASE is a constant; camera_anchor_center/pan_center/pullback_target/clamp_center are pure arithmetic — verify no libm/transcendental crept in.
- The zero-per-frame-heap-churn rule in the input poll: mouse_map's fixed move buffers still fixed; pullback_feed per-frame allocations (if any) — verify.
- The harness-immunity architecture: pullback_feed runs ONLY in the app frame loop (main), all pullback state on App — the harness capture path (harness/) never calls camera_update nor pullback_feed. Spot-check the harness entry points to confirm the claim's structure.

Output path: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r2/architecture.json
