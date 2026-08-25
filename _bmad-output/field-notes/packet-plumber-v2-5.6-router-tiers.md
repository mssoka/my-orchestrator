# Field notes — packet-plumber-v2-5.6-router-tiers

- `tools/harness.sh` builds the rlsw shadow in the worktree (~40s + github clone); a fresh worktree can instead `ln -s` the main checkout's `tools/raylib-sw/shadow` (gitignored) and `ODIN_ROOT=$PWD/tools/raylib-sw/shadow odin build harness -out:bin/harness` — 2nd sighting of the shadow-absent trap.
- Golden re-bless for a catalog change is MECHANICAL + PROVABLE: T2 PNGs must stay byte-identical (git status on goldens/*.png), every .log.bin diff must be EXACTLY the 8 catalog_hash bytes at 17..24, and .t1 shifts only in the catalog_hash header + per-tick hashes (state serialization embeds catalog_hash). Script the byte-check; don't eyeball it.
- The 5.6 placement values moved from the old PLACEMENT_MIN_SEP_TILES const into balance.json (its own comment promised that home on the "next legitimate re-bless") — the const's comment is the roadmap; when a data value is golden-poisoned, the const comment tells you when it can move.
- New demo goldens: identical frame bytes across captures is NORMAL for settled static topologies (place.dem does the same) — don't mistake it for a capture bug; the T1 manifest + replay gate are the real pins.
