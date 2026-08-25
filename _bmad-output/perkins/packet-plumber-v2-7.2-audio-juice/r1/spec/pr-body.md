## Story 7.2 — Audio juice (1–2 stings) `[E8.3, ODN-15]`

Just-enough audio to prove the concept: a crisis-alert sting + a throttled
arrival click, played through raudio, with variant selection from the
**app-owned cosmetic rng** (determinism-neutral), and every audio alert
captioned on-screen.

**Acceptance coverage**

1. **Crisis fires → sting; arrival → click; variant from cosmetic rng only;
   captions shown.** The event hooks consume `Crisis_Triggered` and
   `Packet_Arrived` from the ODN-14 event buffer (the app's per-frame new
   slice; catch-up frames deliver tick-ordered cues). Variant picks draw
   exclusively from `Audio.cosmetic` (a `core.Rng` instance owned by the app,
   seeded with the fixed `COSMETIC_SEED`) — `consumer_consume` has **no
   access to `Run_State` at all** (signature: events + catalogs), so it
   cannot draw from `state.rng` even by accident `[ODN-15]`. Captions: the
   bottom-center caption line shows "crisis alert - <name>" / "packet
   delivered" for 40 ticks (2 s); the caption surface stays live while muted.
2. **New T1 determinism golden; existing suite unshifted; `tools/ci-local.sh`
   9/9.** New `demos/audio.dem` (the 4.2 surge recipe + explicit spawns —
   227 arrivals + 1 crisis trigger in the run) + `goldens/audio.t1` +
   `audio.log.bin`. The harness interleaves the app's real consumer
   (`au.consumer_consume`, same seed) between steps; the replay gate re-sims
   the blessed log **without** the consumer and must reproduce the manifest
   byte-identically — **audio on == audio off**, proven through the real
   ODN-11 path. A `draws > 0` vacuous-guard fails the demo if the consumer
   never drew (negative-controlled: disabling the consume call fails the
   golden). Full suite: 9/9 on macOS native **and** the CI replica container.
3. **PR body carries the module shape, the cosmetic-rng proof, the throttle
   policy, the asset-drop contract, the caption surface.** All below.
4. **Story card status line** updated in `stories-v2.md` (established pattern).

## Module shape

- **Home:** `app/audio/audio.odin` (package `audio`) — the ODN-15 audio layer.
  App-side only; `core/` never sees audio.
- **Lifecycle:** `audio_init` (open the device via `InitAudioDevice`, load the
  6 variant slots) / `audio_destroy` (unload + close) / `audio_reset_run`
  (per-run throttle + caption reset, called from `start_run`). Silent
  fallback: a missing audio device leaves sounds empty — captions still
  caption, nothing plays.
- **Event wiring:** `main.odin` feeds `state.events[audio_mark:]` (the new
  slice, mark-based — the app never drains the buffer, the 4.2 tripwire)
  once per frame to `consumer_consume` (PURE: variant draws, arrival
  throttle, caption state, staged plays), then `audio_flush` plays the staged
  alerts (the only raylib-touching half, gated on device + mute).
- **Mute:** `M` through the 5.4 intent layer (`Toggle_Mute` intent + effect
  hook). Captions stay live while muted — a muted game is not a silent game.

## Cosmetic-rng proof `[ODN-15]`

- Variant pick = `rng_range(&a.cosmetic, 0, N-1)` where `cosmetic` is an
  app-owned `pp.Rng` seeded `0x5EED_A11D0` — never `state.rng`, never any
  sim state. Structural: the consumer's signature takes `events` + `cat`
  only; there is no code path from it to the sim.
- The `audio` T1 golden pins the claim: live run (consumer active) == replay
  of the blessed log (no consumer) == blessed manifest, byte-identical.
  The draw stream is also seeded identically in the harness, so the golden
  exercises the app's real pattern, and the vacuous-guard proves it ran.

## Arrival-click throttle policy

At most **one click per 2 logic ticks** (`ARRIVAL_MIN_GAP_TICKS = 2` =
100 ms at the pinned 20 Hz logic — 10 clicks/s max). A busy tick with 30
deliveries is ONE click, never a buzz. The throttle keys on the *event's*
tick, so catch-up frames stay throttled across their ticks. Suppressed
arrivals are silent **and** uncaptioned (no alert happened). Crisis stings
are not throttled (the crisis engine's per-activation dedup already bounds
them).

## Asset-drop contract

`assets/audio/README.md` documents it: drop SFX files at
`assets/audio/crisis_01.ogg`..`crisis_03.ogg` and
`arrival_01.ogg`..`arrival_03.ogg` (OGG Vorbis recommended; WAV/MP3/FLAC
also load). A slot without a real file loads a **synthesized placeholder**
(alarm beeps / swept click, PCM16 WAV built in memory). The variant count is
FIXED (3 + 3), so the cosmetic draw pattern never depends on which slots are
real — the golden stays valid with or without assets.

**Sources (user rulings 2026-08-17, relayed via Gru):** SFX — the two stings
in this contract — come from **ElevenLabs**; music/ambience comes from
**ElevenLabs Music OR Suno (the user's choice), only if ever needed, NOT in
MVP scope** (the soundtrack is a candidate parallel DistroKid release, out
of story 7.2's contract). Terms notes carried in `assets/audio/README.md`:
(a) paid-plan ElevenLabs outputs are assigned to the user with **perpetual
commercial rights, surviving subscription end**; (b) ElevenLabs SFX outputs
are **sublicensed to other ElevenLabs users BY DEFAULT** — the Sound Effects
page's **Disable** toggle opts out (a to-do when real SFX are generated);
(c) music in a commercial multi-platform game = the **Studio Games** tier in
the ElevenLabs Music Commercial Rights table — a ship-time plan
consideration, not now. No real audio assets were generated or fetched; the
placeholder path is unchanged.

## Caption surface

Bottom-center line above the tray (soft dark pill for legibility), 40-tick
dwell. Crisis: "crisis alert - <catalog display name>"; arrival: "packet
delivered". While muted, the slot shows "audio muted - press M" (alerts
still win during their dwell). This is the minimal a11y seam; story 7.3
builds the full caption system on it.

## Verification

- `tools/ci-local.sh --mac`: **9/9** (incl. the new golden in gate 4, drift
  surface in gate 5).
- `tools/ci-local.sh` (CI replica container): **9/9**.
- App smoke: audio device init (miniaudio/CoreAudio) + all 6 placeholder
  waves decode + load cleanly.
- Negative control: disabling the consumer's consume call fails the golden
  with the vacuous-guard message (then reverted).

## Decisions & rationale

- **Placeholders over blocking on assets** — the briefing's asset contract:
  ship complete with synthesized tones behind a documented drop-in path;
  real files replace slots byte-for-byte. Variant count fixed so the golden
  is asset-independent.
- **Consumer/flush split** — `consumer_consume` is pure (no raylib) so the
  harness golden runs the app's REAL draw pattern (single source of truth),
  while the sw-rendered harness lib (no raudio.o) links clean — Odin DCEs
  the unused audio procs; no `build_raylib_sw.sh` change needed (verified
  macOS + container).
- **A/B via the existing replay gate, not a second loop** — the replay
  re-sim WITHOUT the consumer IS the "audio off" arm; byte-equality through
  the real ODN-11 path is the strongest form of the claim.
- **Tick-based throttle + caption dwell** (not wall-clock) — deterministic,
  freeze naturally under pause, and stay honest with the sim's heartbeat.
- **M routed through the intent layer** (5.4 doctrine) — keyboard-only
  cosmetic like the assist tier; pad/controller mute is full-game settings
  (out of scope per the card's scope guard).
- **Out of scope, deliberately:** soundtrack, ambience, mixer UI, settings
  page, non-ASCII caption glyphs (draw_text truncates runes to bytes).



