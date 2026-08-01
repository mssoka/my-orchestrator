# finlit-prototype — field notes (badge-out shard)

- Godot 4.7 gotchas that bit: `trait` is a RESERVED word in GDScript; `theme_override_constants/separation` is tscn-serialization syntax only — at runtime use `add_theme_constant_override()`; JSON.parse turns ALL ints into floats, so save-load needs an explicit re-cast pass before array indexing.
- DeepSeek `deepseek-v4-flash` has THINKING ON BY DEFAULT and it silently eats max_tokens (kid answers truncate mid-sentence) — send `"thinking": {"type": "disabled"}` for short-form output; docs 302-redirect, use web_search snippets instead of web_fetch.
- `godot --headless --check-only <project>` is NOT a valid invocation and hangs for 120s+; the working headless gate is `godot --headless --path <dir> --import` then `--quit-after 600`, tests via `--script res://tests/x.gd` with `extends SceneTree` + `_initialize()`.
