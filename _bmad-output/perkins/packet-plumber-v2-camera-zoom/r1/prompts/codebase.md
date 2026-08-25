--- YOUR LENS (source tag: codebase) ---

Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Specific seams to verify in this diff: rnd.from_screen / rnd.view_compute / rnd.camera_* helpers the new code calls; the existing 7.1 eased-camera fields (cam_zoom/cam_wx/cam_wy + the *_to targets) on App and how camera_update consumes them; the wire_test_topo / wire_test_cat fixtures the new input tests reuse; the noc_key_test precedent the new tests claim to follow; NOC_PANEL_X/Y/W/H constants used by the new noc_panel_hit; and whether any OTHER wheel reader (e.g. in the harness or release render path) still exists after the old render-block read was deleted.
