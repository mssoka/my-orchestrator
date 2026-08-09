# Field notes: packet-plumber-blender-art

- 2026-08-08: **NEVER call `bpy.ops.wm.read_factory_settings()` via BlenderMCP.** It reloads the
  BlenderMCP addon, which KILLS the :9876 socket server thread and does NOT restart it — Blender
  (PID) keeps running, but port 9876 has no listener and every MCP call then fails "Not connected to
  Blender" / "Connection closed". Chicken-and-egg: you can't run Blender code to restart the thread
  because the connection is dead, so it's a user-blocking halt. To clear the default scene, DELETE
  the default objects instead (`bpy.data.objects.remove` loop over Cube/Light/Camera + purge orphan
  data), never a factory-settings reload. Recovery = user toggles the BlenderMCP addon off→on in
  Blender Preferences → Add-ons (or its N-panel Start Server) to respawn the listener.
- 2026-08-08: Blender 5.2 LTS / Eevee Next has NO built-in bloom (`eevee.use_bloom` removed in 4.2).
  The "glowing flows on dark canvas" glow must come from a **Compositor Glare node** (Bloom) on the
  render output, with Standard view transform so the canon's exact hex values read faithfully (AgX
  / Filmic desaturate bright emissives).
- 2026-08-08: **Blender 5.2 compositor API (big refactor).** `scene.node_tree` is GONE (PR #143619).
  The compositor is a node-GROUP now: `nt = bpy.data.node_groups.new(name, 'CompositorNodeTree')`;
  `scene.compositing_node_group = nt`; output via a `NodeGroupOutput` node + `nt.interface.new_socket('Image', in_out='OUTPUT', socket_type='NodeSocketColor')`; assign Render Layers → Glare → GroupOutput. The Glare node's settings are **input sockets** with DISPLAY-NAME enum strings (`'Bloom'`/`'Fog Glow'`/`'Streaks'`, `'High'`/`'Medium'`), NOT node properties and NOT `'FOG_GLOW'`/`'HIGH'`. `CompositorNodeComposite` is undefined in 5.x.
- 2026-08-08: **To DISABLE the compositor in 5.x you must null the group:** `scene.compositing_node_group = None`. Setting `scene.use_nodes = False` alone does NOT stick (it stays True while a group is assigned) — a stale Glare group from a prior build silently re-applied and BLEW a light/daytime render to pure white. Symptom: PNG bg samples (1,1,1) instead of the set cream.
- 2026-08-08: Eevee BLEND transparency renders an Emission-through-Transparent mix as NOTHING (the glow disc vanishes). Opaque fade-to-canvas halos read as visible dark discs (they occlude the grid). Net: for glow, use compositor Bloom (dark palette) or just flat emissive (light palette) — don't fight Eevee's blend pipeline. Standard view transform keeps chroma (AgX desaturates bright hues to white); emissive strength ~1.0 = faithful hex, >1 clips channels toward white/cyan.
- 2026-08-08: **Verify a lavish verdict in `~/.lavish-axi/state.json` (sessions.<id>.chat) before acting** on a load-bearing decision — the poll's `prompts[]` usually delivers, but session-end can strand a queued message and the printed `prompts[]` line is ambiguous to parse; state.json chat is ground truth. (Confirmed the user's canvas verdict "light" there before rendering the rest.)
- 2026-08-08: For a "house" silhouette in a 3/4 ortho render, build a **gable (ridge) roof and run the ridge along Y** so the triangular gable-END faces the camera (-Y); ridge along X makes the camera see a roof slope and the building reads as a flat cube. In-scene TEXT labels must be rotated vertical (X 90°) to face the camera — flat-on-ground text foreshortens and overlaps geometry.
