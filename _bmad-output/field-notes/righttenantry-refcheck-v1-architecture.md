# Field notes: righttenantry-refcheck-v1-architecture

_2026-07-29 · recorded by Gru from the minion's badge-out report (seed
entry — shards are normally minion-written)._

- lavish HTML builds: piping large markdown through `marked` via
  subprocess stdout truncated the artifact at ~85KB (pipe-buffer issue).
  Build via a file write, then verify byte length + tail-section presence
  before serving. Found only after the user reviewed a page truncated
  around §7.3 — verify BEFORE serving.
- `npx -y lavish-axi <file>` opens the user's browser itself; there is no
  URL to discover or relay.
- Keep one foreground poll per lavish session; if it dies, re-run —
  queued feedback is never lost. Never `lavish-axi stop` (shared server,
  port 4387 — kills every minion's session).
