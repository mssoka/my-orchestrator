# packet-plumber-v2-visibility

- App-layer HUD surfaces (draw_hud) are T2-INVISIBLE by construction — the harness capture path never calls draw_hud; zero golden shift needs no fold. Verify app-layer overlays with a scratch replica (rlsw shadow + LoadImageFromScreen) + PIL pixel-scan, never eyeball — the 5.3 addendum recipe, and it caught the pool bar fill at the exact right rect.
- Bundle SLOTS renumber on every topology change (bundles_rebuild in pipe-slot order) — any cross-tick bundle reference (drop-marker rings, etc.) must store + verify the canonical (lo,hi) node pair, never the slot.
- The 2.3 silent severance cull counts an SLA drop with NO event + NO Drop_Site — a why-dropped split fed only from drop_sites UNDERCOUNTS after demolitions; derive the residual (dropped - pool - queue) as "severed".
- Review swarms earn their cost: both hunters independently caught the severed undercount; the edge hunter caught the bundle-slot misanchor. `make([dynamic]T, 0, N)` has LENGTH 0 — a `counts[p.class]` guard `p.class < len(counts)` silently writes nothing (test passed only because it used a fixed [8]u32).
