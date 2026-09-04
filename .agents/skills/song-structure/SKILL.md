---
name: song-structure
description: Analyze a song's structure — section boundaries, energy profile, BPM, drum activity — from any audio file, for music-video scene planning. Use when splitting a song into 30-second (or other length) video scenes, mapping lyrics sections to timestamps, finding the stripped-down bridge or the drop, or when the user asks to analyze audio/MP3 structure for a video project.
---

# song-structure — audio structural analysis for music-video planning

Bundles `scripts/section_scan.py` (numpy + scipy + ffmpeg, no librosa needed).
Given any audio file it prints a segment table — start, end, length, energy
(dB), spectral centroid, bass share, onset density — plus a BPM estimate.
The agent's job after running it: read the table, map segments to song
sections using the lyrics + energy fingerprints below, and cut scenes.

## Run

```bash
python3 <skill-dir>/scripts/section_scan.py <song.mp3> \
    [--min-sec 12] [--json out.json]
```

- `--min-sec` — minimum section length (default 12s; use ~15 for anthems,
  ~8 for songs with fast section turnover).
- `--json` — also write machine-readable output (keep beside the video
  project's shotlist as the ground truth for scene cut points).
- Requires: `ffmpeg` on PATH, `python3` with `numpy` + `scipy`.

## Reading the output

| Column | Meaning | Use it for |
|---|---|---|
| start/end/len | Segment bounds | Scene cut points |
| dB | Mean RMS energy (log, 0 = loudest) | Loud vs stripped sections |
| cent (Hz) | Spectral centroid | Bright skank/horns vs dark intimate vox |
| bass | Share of energy <150 Hz | Dub bassline presence — chorus/drop marker |
| ons/s | Onset density | Drum activity — one-drop feel, drops, outros |

## Fingerprint guide (map segments → sections)

With the lyrics in hand, label segments by character:

- **Intro** — first segment(s), low dB, low onset density, often low bass.
- **Verse** — moderate dB, onset density steady (one-drop pulse).
- **Pre-chorus** — short (~8–15s), energy stepping UP into the chorus.
- **Chorus** — local dB maxima, brighter centroid, often more bass (full mix).
- **Bridge/stripped** — mid-to-late song energy MINIMUM (dB dip), sparse onsets.
- **Drop** — sharp energy jump right after the dip, high onset density.
- **Final chorus** — post-drop energy plateau, usually the global dB max.
- **Outro** — last segment, fading dB, sparse onsets (whispers/echo tails).

Energy usually steps up pre-chorus → chorus and the novelty peaks ARE the
section boundaries; trust a boundary more when dB and onsets/s shift
together across it.

## Music-video workflow hookup

1. Run the scanner with `--json` into the video project dir.
2. Label segments against the lyrics (fingerprints above).
3. Cut scenes: one scene per section, merging short neighbors until ~90% of
   scenes land within ±5s of the target scene length (e.g. 30s).
4. Each scene row in the SHOTLIST carries: section, real timestamps,
   lyric beats, blockout spec, camera, and the generation prompt.

BPM sanity check: the estimate should match the song's stated BPM
(reggae one-drop at 70–80 BPM lands cleanly). If it reads ~2x, halve it.
