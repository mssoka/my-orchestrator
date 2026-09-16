# Song → native artwork

## Minimum creative record

Use supplied lyrics/brief and an actual understanding of the song. Record:
- Emotional/theme evidence, not merely a genre label.
- One visual metaphor and the physical mechanism that expresses it.
- What moves, what stays legible, and why the full motion/light state repeats.
- Palette roles: structural neutral, accent, key/rim, warmth/energy; explain each connection to this song.
- Camera/composition, intended motion character and a thumbnail phase.

A warm/cool palette from another song is an example of reasoning, not a channel rule. Scripts neither infer these decisions nor certify beauty. Avoid an obligatory six-render comparison workshop. Reuse an existing approval.

If cuts or motion require structural/tempo evidence, use the installed `song-structure` skill. Distinguish measured/approximate BPM, failed scans and user-provided timing. This package contains no beat detector and claims no exact synchronization.

## Two authoring paths

**Existing native scene:** configure `art.mode=scene`, `scene_file`, `scene_name`. The input stays unchanged. It must have its intended camera, square pixels, opaque16:9 framing, a validated sRGB display output, and genuinely periodic motion over `loop.frames`, starting at that scene's existing start frame. Artwork intake is3D only: no VSE or speaker audio. Missing/special external dependencies stop; existing external assets are reported, not automatically bundled. Keep original music for the edit stage.

**Native helpers/recipe:** `scripts/recipe.py` exposes `linear_hex`, `material`, `box`, `annulus`, `periodic`, `area`, and `build(config)`. The radial-relief recipe distils the radial mechanism, compact periodic controls and lighting/material patterns of the production workflow; it is a neutral starting mechanism, not a universal art style or the same song-specific Iris.

For live authoring, first checkpoint the current Blender document to a private owned path, retaining dirty/unnamed work. Use Blender MCP to import the helper module from its absolute skill directory. `build(config)` adds a new scene; it never deletes the old one. Inspect/edit the native objects, camera and lights. Save the selected scene as a **new** `.blend` outside the later job output root; use scene intake for production. Never run `native.py`'s background-worker entry point in a live document.

For a new concept, build its geometry with ordinary Blender/Python and these small helpers, rather than adding a new workflow engine. Save a selected editable scene and enter through the same scene intake. Only add a recipe switch when the concept is genuinely reusable and a small native test proves it.

## Loop judgment

Use one full state period, not a shorter half-cycle or several repetitions. Express native controls with integer-cycle sin/cos or cyclic animation; short expressions/property targets avoid Blender's driver string-length limit. Geometry, light positions/energies and any material animation must all return. A unique marker can make a mechanism's long cycle legible.

Preview several actual phases and low-resolution motion before a full native loop. Encode exactly the intended unique frames; render the next endpoint separately for comparison, never append a duplicate closure frame. Inspect winding/normals, camera margin, contact shadows, material separation, clipping, and the actual seam. Numbers help find mistakes but cannot judge the song fit.

The agent may perform routine technical/pixel review under the user's direction. `review` records what was actually observed; it is not a fabricated user verdict or another approval ceremony.
