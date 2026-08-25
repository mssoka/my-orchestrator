--- YOUR LENS (source tag: architecture) ---

Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

Round-specific architecture invariants (from the project context + round briefing): ODN-1 (core/ is pure — vendor:raylib only in app/; the sim never sees the camera), ODN-12 (the intent layer: device event → map → intent → executor → app effect hook), ODN-13 (no globals — everything off App), the §10.4 no-transcendentals rule on the rasterized path, the zero-per-frame-heap-churn rule in the input poll, and the "one consumer" rule for the wheel (effect_zoom owns the NOC-panel-vs-zoom policy). Verify the diff respects the layering: camera math in app/render/camera.odin (pure float math), effects in app/main.odin, intents/exec in app/input/.
