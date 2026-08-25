# packet-plumber-terminal-assets-5.11 — field notes

- The 7.1 sprite pipeline regen (Blender headless) is PIXEL-IDENTICAL but PNG-encoding NON-DETERMINISTIC run-to-run — after adding sprites, `git checkout` the existing PNGs so only new files + sprites.json land; bboxes are stable so the manifest diff stays additive.
- Extending the sprite sheet REQUIRES mirroring `SPRITE_COUNT` + the `files` list in app/render/sprites.odin (sprites_parse_boxes rejects len(order)!=SPRITE_COUNT and the whole sheet falls back to primitives = golden shift) — that's sheet/manifest data, distinct from role→index draw wiring (5.11's).
- The canon blend (`art-renders/blend-sources/pp-scene-light-vista.blend`) opens + re-saves cleanly via headless Blender (`bpy.ops.wm.open_mainfile` + `exec(open("pp_lib.py").read())` then save_as_mainfile) — the provenance path for "the blend gains new models".
