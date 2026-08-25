# packet-plumber-v2-3.4-sla — field notes

- Span trap: test-seed fixture nodes sit 12 tiles apart — a `narrow` pipe draw is silently REJECTED (max_span 10) → no route → packets pile at their source with zero events; for narrow-tier tests, spawn nodes ≤10 tiles apart. Cost me a debug probe cycle.
- `record_run` clears `state.events` every tick (ODN-14 drain) — any end-of-run event scan is vacuous; collect the stream while stepping (the `sla_record_run` pattern returning hashes + events).
- Cumulative-loss breach is NOT monotone: later deliveries dilute the ratio below tolerance, so a transition-style Exit would fire falsely — the Loss latch must be sticky-Enter by contract; "monotone" applies to the counter, never the ratio.
