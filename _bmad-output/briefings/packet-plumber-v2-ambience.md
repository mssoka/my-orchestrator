# packet-plumber-v2-ambience

## Task

Integrate the user's Suno ambient bed into the game. User expectation
(2026-08-23): "i dont hear the ambient suno song" — the track should
play in-game. Asset: `Warm Analog Drift.wav` (PCM s16le 48kHz stereo,
3:04) — vaulted at `/Users/moses/code/_local-refs/audio/Warm Analog
Drift.wav` with README (provenance + this contract). The user's
fun-test verdict is IN by expectation: it sticks.

## Scope

1. **Asset in**: bring the track into the repo as a game asset
   (`assets/audio/` — new dir). The 35MB WAV is the SOURCE; ship a
   compressed form for runtime if raylib supports it (OGG via ffmpeg —
   ~3–5MB) — minion's call; keep the WAV source in the repo only if
   size-reasonable, else document the transform from the vault path.
2. **Loop seamlessly**: trim/loop to a clean ~2min seamless loop
   (the vault README's contract — no audible seam at the wrap point).
3. **Duck under event sounds**: #81's wire clicks + spawn chimes MUST
   stay clearly audible — the bed sits low (sidechain-style ducking if
   the audio layer supports it, else a conservative fixed level).
4. **Placement**: calm, MM-pace — starts with the run, gentle on the
   title screen if trivial, sane behavior on pause (keep playing low,
   or soft-mute — minion picks, document; NOT a hard cut).
5. **Volume knob**: expose master music volume as a named tunable
   (and a mute flag) — the user will tune by ear.

## Rules (hard)

1. **Presentation-only**: audio never touches the sim. T1/T2/replay
   .log.bin byte-identical; NO golden changes (no visual change) — if
   any golden moves, that's a bug.
2. **Determinism-safe audio init**: no audio-device failure may crash
   a headless/CI run — the harness path must survive "no audio device"
   (the #81 event-sound precedent: verify how it handles headless and
   match it).
3. **Respect #81's event system**: don't rebuild it — layer beside it
   (the append-only event tags stay the SFX path).
4. The vault README's mood plan is recorded for later (intensity
   layers → flow/tension/crisis via existing state hooks) — OUT OF
   SCOPE here; single bed only. Note it as the stage-3 candidate.

## Acceptance

- `odin run app` plays the bed; seamless loop (no audible wrap seam);
  event sounds clearly audible over it.
- Named volume/mute tunables work.
- T1/T2/replay hash-equal; zero golden diff; headless/CI runs clean
  with no audio device.
- PR body: loop points used, ducking approach, asset sizes.
- pr_review: 1.

## Skills policy

bmad-quick-dev.

## Model policy

deepseek-v4-flash, --thinking max.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-ambience
- base: v2 (fresh head at dispatch)
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- merge order: free (no golden storm; minor app/main.odin overlap
  risk vs font-overhaul — coordinate with Silas, rebase-on-demand)
