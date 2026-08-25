# packet-plumber-v2-node-clarity — field notes (minion shard)

- **Odin #load embeds data files at COMPILE time** — after any palette.json
  token edit, REBUILD the harness before re-rendering (a stale embed silently
  renders old colors and wastes a re-bless cycle).
- **The blur-gate sampler must be calibrated before trusting it**: build the
  σ6 sampler first, confirm it reproduces the audit's baseline deltas (res↔
  sbiz ~3-4°, res↔campus ~13°, router↔host ~9.7°) on the OLD golden, then
  iterate. Offline PIL sprite-composition sims under-predict the real
  render's saturation (real board surroundings darken/mix) — screen with the
  sim, settle with real renders. Wash alphas encoded in the token's alpha
  byte keeps everything in data (palcheck-pinnable).
- **Warm-family clustering is the trap**: terracotta↔brick↔warm-stone all
  blur toward the cream canvas (~44°) — the ≥15° bar forces a genuinely cool
  stone (green-gray ~110°) and a desaturated brick. Palette-anchor "families"
  survive, literal anchor hexes don't. Keep token edits ADDITIONS-ONLY when a
  sibling job owns shared tokens (POP owns the network) — and re-emit
  palette.json in its original aligned format (json.dump reformat churns 700
  lines).
