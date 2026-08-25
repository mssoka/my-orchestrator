# field-notes — packet-plumber-v2-ux-font-resize (2026-08-15)

- macOS compositor FREEZES the GL front buffer for occluded windows — `rl.TakeScreenshot`/`LoadImageFromScreen` repeat frame 1 forever; the reliable capture is a RenderTexture pass + `LoadImageFromTexture` readback AFTER `EndTextureMode` (the GL flush — a read inside texture mode returns the stale FBO).
- Bundled-font determinism works: LoadFontEx on a committed static TTF (fonttools-instanced Open Sans) renders the same atlas in rlsw + GPU; a font swap folds T2 text goldens but leaves T1 untouched — verify `.t1`/`.log.bin` show zero diffs.
- Pre-existing v2 HUD overlap: the top-left title/hint ran UNDER the centered health card at 1280×720 (the card is drawn after, alpha 240) — pixel-scan ink extents to prove overlaps before/after; resize anchors must use `view.win_w/h`, never the WIN_W/WIN_H constants.
