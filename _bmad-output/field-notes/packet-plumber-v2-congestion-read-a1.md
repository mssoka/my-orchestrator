# field notes — packet-plumber-v2-congestion-read-a1

- 2026-08-28: palcheck render-only fixtures — `crisis.pipe_congestion` has len 0 until warnings_update runs; `resize()` + explicitly zero the grown slots to `.None`, and remember E26 rejects terminal→terminal pipes in fixtures (mirror §7: terminal→router).
- 2026-08-28: when a band-measure palcheck leg returns exactly your scan half-window count (2·half+1), the scanner is measuring ALONG the feature, not across it — assert a predicted pixel count from the draw's own math first (dump the column) before trusting the leg.
- 2026-08-28: stride the evidence harness FIRST (bin/harness_before from HEAD + view-only extension), then mutate — the corpus-freshness + mutation-leg ordering (before-strips → change → re-bless → after-strips) made every A1 claim mechanically checkable without a second worktree.
