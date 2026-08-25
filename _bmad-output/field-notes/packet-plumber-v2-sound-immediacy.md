# packet-plumber-v2-sound-immediacy — field notes

- **Event-stream re-bless = the 4.2-class cost, cause-documented:** adding two
  zero-payload append-only event tags (PIPE_DRAWN/NODE_SPAWNED) moved 44 T1
  manifests; ZERO pixels/logs changed (verify with `git status` before claiming
  the re-bless is pure). Divergence ticks line up exactly with first-draw/
  first-spawn ticks — that's the cause check.
- **The live fast-path emits the SAME wire event as replay, at the SAME
  apply_tick** (`inp.tick + 1` — the logged apply_tick): emit from BOTH
  step's command loop and commit_draw or the app's stream silently diverges
  from a log replay (audio on == audio off holds only if the events match).
- **Input struct field name collision:** `Input.events` is already the
  Device_Event scratch buffer — name the app-side event ref `sim_events`
  (the `ictx.events[:]` dispatch call shadows any field named `events`).
- Parity (drive_parity) dispatches ALL frames BEFORE its step loop — a
  dispatch-time event lands before the hash mark and never rides the pinned
  stream; keep `sim_events` nil there (input-parity is not the audio golden).
- Brush's frequency-stack rule (DIRECTION §3) maps to synth recipes directly:
  wire = falling low-mid "tock" (opposite direction of the arrival's rising
  sweep so they're distinguishable), spawn = low thump + mid body + high tick.
