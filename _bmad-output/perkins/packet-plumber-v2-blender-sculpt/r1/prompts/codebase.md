--- YOUR LENS (source tag: codebase) ---

Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Pay attention to: app/render/sprites.odin callers of the changed procs (sprite_shadow, shadow_for_role, shadow_for_puck, sprite_house_target, sprite_campus_target), the sprites.json binding in sprites_parse_boxes, and the tools/ scripts' cross-references (sprite_guard, SPRITE_ORDER, SPRITE_SPECS).
