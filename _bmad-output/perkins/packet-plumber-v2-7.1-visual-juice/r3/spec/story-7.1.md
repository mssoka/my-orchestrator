### Story 7.1 — Visual juice (light-canvas polish)

- **Slice:** 7 · **Epic(s):** E8.1, E8.2 · **Systems:** View polish `[ODN-1]`.
- **Goal.** The light-canvas canon (warm-cream map, glowing pipes, colored packet dots, node
  health colors, leak spray) at just-enough quality; UI chrome (gauges, forecast, alerts) with
  progressive disclosure + filter/focus + alerts-as-nav.

**Given/When/Then:**
- **Given** the view layer + the look-book palette;
- **When** the game renders;
- **Then** the View reads **only snapshots** (never perturbs the sim) `[ODN-1]`; crisis events
  drive matching juice; packet type/node state are never color-alone; the viewport scales so
  wider/taller screens reveal more map (camera-fit).

- **Edge-case contracts:** `[ODN-1]` view-reads-snapshot, never-color-alone. **Golden:** T2 of
  the juiced frame.
- **Launchable increment:** the game feels like saving the internet.
- **Status:** implemented 2026-08-17 — PR open (the lavish-gated visual direction: top-down
  Blender sprite buildings + tier-band pipes with inset lanes + the focus-zoom camera +
  filter/focus + alerts-as-nav + doorstep queues; the `juice.dem` T2 golden; the look-book
  §6 amendment records the surface ruling; 74 existing T2 frames deliberately re-blessed).

