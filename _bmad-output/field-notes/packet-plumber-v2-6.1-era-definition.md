# Field notes — packet-plumber-v2-6.1-era-definition

- The action-log header stores the run's ERA at write time; a mid-run era advance means the header MUST carry the RUN-SETUP (start) era — `log_write` gained a `header_era` param (harness passes demo.era) — or the replay's advance command validates `to_era <= era` (already 3 from the header) and latches replay_error.
- eras.json's parse sits AFTER the PROTO required-content guards: a pkt doc that drops email/streaming must surface the packet_types rejection, NOT an eras-row "unknown packet type" — catalog load-order is a test-contract surface, keep new cross-ref catalogs last.
- E14 deferral tests: never hand-append Active_Crisis rows — the engine auto-resolves them (Saturated_Bundle needs a live saturated bundle; Pool_Exhaustion clears when the pool is below cap). Build a REAL crisis (narrow fixture + era-3 surge on schedule) or the deferral window silently collapses.
