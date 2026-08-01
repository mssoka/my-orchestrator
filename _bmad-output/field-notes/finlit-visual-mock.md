# finlit-visual-mock — field notes

- Godot: theme does NOT propagate across a CanvasLayer — popups under
  `PopupLayer` render default-white text unless you hand them the theme
  (`card.theme = theme` in `_open_popup`). Found via blank-looking captures.
- Container layout is deferred: styling/animating a node the same frame it's
  `add_child`ed gives `size == (0,0)` — juice pivots must await `resized`;
  and `get_child(i)` right after a rebuild hits queue_free'd nodes (new
  children are appended AFTER the dying ones until frame end).
- Screenshot rig: `--headless` has no renderer (blank PNGs); run windowed
  with `--position -3000,-3000` to stay off the user's screen — rendering
  still works. `set_process(false)` freezes game timers for deterministic
  stills; seed states via the pure economy API, never clicks.
