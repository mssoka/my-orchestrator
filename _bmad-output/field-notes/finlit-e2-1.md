# Field notes — finlit-e2-1 (playtest protocol)

- Godot disabled Buttons swallow clicks AND emit no `gui_input` (windowed probe: enabled=2 hits, disabled=0); headless `Input.parse_input_event` never routes GUI at all — tap capture needs a transparent `MOUSE_FILTER_STOP` overlay child (anchors FULL_RECT), verified windowed; headless tests pin wiring via direct `gui_input.emit`.
- Godot `FileAccess` WRITE buffers: `get_file_as_string` right after `store_line` is empty until `flush()` (probe it — same trap as pipe truncation); `DirAccess.make_dir_recursive_absolute` handles `user://` paths fine.
- GDScript 4.7 gotchas: no `Array.find_last` (use `rfind`); `:=` on a String/Array ternary trips INFERENCE_ON_VARIANT warnings-as-errors (annotate `: Array` explicitly); `Time.get_datetime_string_from_system(false, true)` puts a SPACE in filenames (use UTC + replace ":").
