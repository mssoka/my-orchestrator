--- YOUR LENS (source tag: codebase) ---

Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Specific seams to verify in this diff (each is a claim the diff makes about the surrounding codebase — open the files):

- rnd.from_screen / rnd.view_compute / the View fields (scale/off_x/off_y/win_w/win_h/world_w/world_h/tile_px/lane_detail) the new camera code reads.
- The existing 7.1 eased-camera fields (cam_zoom/cam_wx/cam_wy + the *_to targets) on App and how camera_update consumed them BEFORE this diff (the base is in the worktree's git history — `git show <base>:app/main.odin` if needed; base = the PR's merge-base with v2).
- The wire_test_topo / wire_test_cat / TEST_LOGIC_HZ fixtures the new input tests reuse (app/input/), and the noc_key_test precedent the new tests claim to follow.
- The settings_effect/app-test precedent pullback_test.odin claims to follow (app/ tests constructing a minimal App).
- NOC_PANEL_X/Y/W/H constants used by the new noc_panel_hit (app/render/noc_overlay.odin) — same constants the panel draw uses?
- pp.node_slot / pp.topology_spawn_node / pp.Event{tag=EVENT_TAG_NODE_SPAWNED} / growth_groups.new_area_seed_tiles / node_kind/node_alive/node_pos — the core symbols the derived SEED classifier reads; and the core's own estate predicate (growth_seed_sep_ok or equivalent) — is camera_spawn_is_seed really its exact mirror (>= floor from EVERY live terminal, terminals only)?
- The core growth doctrine constants: radius_tiles (5?) vs new_area_seed_tiles (10?) — the "gap leaves no third class" claim.
- camera_fit in main.odin vs the fit derivation inside camera_update and view_compute — the "ONE source" claim: is the same min() expression triplicated or extracted?
- Whether any OTHER wheel reader (GetMouseWheelMove) still exists anywhere in app/ or harness/ after the old render-block read was deleted (the e2e/harness paths excepted if PP_DEBUG-gated and pre-existing).
- Whether the input-parity runner (harness/ or tools/) constructs Input WITHOUT the new on_pan/on_zoom hooks (the nil-hook no-op claim the parity contract depends on).
- The Mouse_Wheel/Zoom additions vs the existing Device_Event/Intent unions — any consumer that switches over the unions exhaustively and now misses a case (Odin `case:` fallthrough would catch it — look for or_else-free exhaustive switches that might now behave differently).
