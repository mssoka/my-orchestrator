# packet-plumber-routing-bandwidth-cost — field notes

- 2026-08-13 (routing-bandwidth-cost): a catalog FIELD addition re-blesses
  EVERY .t1 + .log.bin via the cat.hash fold — but it is PROVABLE fold-only:
  splice the OLD catalog_hash over new state-dump bytes 33..40, FNV must equal
  the old golden tick-1 (all 16 demos did); .log.bin diffs were exactly the 8
  header bytes; T2s never moved. Re-bless WITH that proof, not on assertion.
- 2026-08-13 (routing-bandwidth-cost): mixed-tier bundles price at the FATTEST
  member (min tier cost) — per-pipe min relaxation must match the ECMP
  equality test (`dist[v] + min_cost == dist[u]`), or a later cheaper member
  breaks the condition (unroutable). Two-pass collection (min cost first,
  then equality) is the deterministic shape.
- 2026-08-13 (routing-bandwidth-cost): narrow-tier test geometry needs spans
  <= 10 (max_span!) — the 2.2 diamond's 13-spans reject at draw; compact
  diamond (8,15)/(16,11)/(16,19)/(24,15) is narrow-legal. And Odin fmt strings
  need `{{`/`}}` for literal braces in expectf messages.
