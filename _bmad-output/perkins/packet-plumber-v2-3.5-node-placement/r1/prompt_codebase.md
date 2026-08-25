Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match? (e.g. pp.pipe_tier_index, pp.topology_apply_edit, rnd.tray_chip_rect, rnd.tray_router_types, rnd.tray_chip_count, rnd.from_screen, node_type_index, topology_spawn_node, node_slot, node_alive, node_kind, node_pos, node_type, pipe_alive, pipe_a, pipe_b, pipe_id, run_init, log_write, log_read, record_run, clone_log, test_seed_fixture, test_catalog, topo_setup, node_count, pipe_count)
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?
- Check the render package: do palette colors used in new code exist (p.router_body, p.ghost_ok, p.ghost_bad, p.ink, p.ink_soft)? Does View have win_w/win_h? Do node_types entries have `id` and `kind` fields? Is `tier.id` a field on pipe tiers?
- Check the golden re-bless: are the changed .log.bin files byte-different ONLY in the version field (verify with git show 666b082^:goldens/X.log.bin vs the worktree file)? Are pre-existing .t1 manifests and T2 PNGs truly untouched? Is the place.t1 catalog_hash consistent with the current catalogs?
