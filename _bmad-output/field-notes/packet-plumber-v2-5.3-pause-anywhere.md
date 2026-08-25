# Field notes — packet-plumber-v2-5.3-pause-anywhere

- Pause is DRIVER-level, never core: the harness's wall-tick virtual clock
  (one T1 hash per wall tick; sim steps only unpaused; mid-pause commands
  lower to apply_tick = next EXECUTED sim tick) is the pattern; the app shows
  fast-path edits instantly while the harness defers to the step boundary —
  two models, converging at boundaries; the T1 pins the SIM freeze, the log
  pins the edits (don't bless "state stable" claims that include the
  fast-path channel).
- The first paused wall-tick hash legitimately differs from the last stepped
  tick's hash (the stepped hash includes that tick's event stream, drained
  right after) — the stable-window check must baseline on the FIRST paused
  hash, never the previous wall tick.
- App trap: the render reads DERIVED bundles (rebuilt only inside step) — a
  fast-path edit while paused was invisible until resume; needs a
  gen-checked bundles rebuild in the paused render path (derived only).
