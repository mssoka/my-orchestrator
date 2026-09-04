#!/usr/bin/env python3
"""section_scan.py — structural analysis of a song for music-video scene planning.

Decodes any audio file via ffmpeg, then computes:
  - RMS energy envelope (log dB)
  - Spectral flux (onset strength)
  - Spectral centroid (brightness)
  - Bass ratio (<150 Hz energy share)
  - Onset-density per segment (drum activity)

Detects section boundaries via a novelty function (energy steps + flux peaks),
then describes each segment so a human can map segments to song sections
(intro / verse / pre-chorus / chorus / bridge / drop / outro).

Also estimates BPM via onset-envelope autocorrelation.

Usage:
    python3 section_scan.py <audio> [--min-sec 12] [--json out.json]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

import numpy as np
from scipy import ndimage
from scipy.signal import find_peaks

SR = 22050
WIN = 2048
HOP = 512
FPS = SR / HOP  # frames per second (~43)


def decode(path: str) -> np.ndarray:
    """Decode audio to mono float32 via ffmpeg pipe."""
    cmd = [
        "ffmpeg", "-v", "error", "-i", path,
        "-ac", "1", "-ar", str(SR), "-f", "f32le", "-",
    ]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def stft_mag(x: np.ndarray) -> np.ndarray:
    """Magnitude STFT with a Hann window; returns (freqs, frames)."""
    window = np.hanning(WIN).astype(np.float32)
    n_frames = 1 + (len(x) - WIN) // HOP
    idx = np.arange(WIN)[None, :] + HOP * np.arange(n_frames)[:, None]
    frames = x[idx] * window
    spec = np.abs(np.fft.rfft(frames, axis=1)).T  # (bins, frames)
    freqs = np.fft.rfftfreq(WIN, 1.0 / SR)
    return freqs, spec


def smooth(y: np.ndarray, sigma_s: float) -> np.ndarray:
    return ndimage.gaussian_filter1d(y, sigma=sigma_s * FPS)


def estimate_bpm(flux: np.ndarray) -> tuple[float, float]:
    """Onset-envelope autocorrelation BPM estimate in 60-160 range."""
    f = flux - flux.mean()
    ac = np.correlate(f, f, mode="full")[len(f) - 1 :]
    ac /= ac[0] + 1e-9
    lag_min = int(60.0 / 160.0 * FPS)
    lag_max = int(60.0 / 60.0 * FPS)
    lags = np.arange(lag_min, min(lag_max, len(ac)))
    if len(lags) == 0:
        return 0.0, 0.0
    peaks, props = find_peaks(ac[lags], prominence=0.02)
    if len(peaks) == 0:
        return 0.0, 0.0
    best = peaks[np.argmax(props["prominences"])]
    lag = lags[best]
    bpm = 60.0 * FPS / lag
    strength = float(props["prominences"][np.argmax(props["prominences"])])
    return round(bpm, 1), round(strength, 3)


def analyze(path: str, min_sec: float) -> dict:
    x = decode(path)
    dur = len(x) / SR
    freqs, mag = stft_mag(x)

    rms = np.sqrt((mag**2).sum(axis=0) + 1e-12)
    rms_db = 20 * np.log10(rms / (rms.max() + 1e-12))
    rms_s = smooth(rms_db, 0.8)

    flux = np.maximum(np.diff(mag, axis=1, prepend=mag[:, :1]), 0).sum(axis=0)
    flux_s = smooth(flux, 0.15)

    centroid = (freqs[:, None] * mag).sum(axis=0) / (mag.sum(axis=0) + 1e-12)
    centroid_s = smooth(centroid, 1.5)

    bass_mask = freqs < 150
    bass_ratio = mag[bass_mask].sum(axis=0) / (mag.sum(axis=0) + 1e-12)
    bass_s = smooth(bass_ratio, 1.5)

    # Novelty: energy steps (|d rms|) + flux peaks, both normalized.
    d_rms = np.abs(np.gradient(rms_s))
    d_rms /= d_rms.max() + 1e-9
    flux_n = flux_s / (flux_s.max() + 1e-9)
    novelty = smooth(0.6 * d_rms + 0.4 * flux_n, 0.5)

    peaks, props = find_peaks(novelty, prominence=0.08, distance=min_sec * FPS)
    order = np.argsort(props["prominences"])[::-1]
    bounds = sorted({0, int(dur * FPS), *[int(peaks[i]) for i in order[:14]]})

    def seg_stats(a: int, b: int) -> dict:
        onset_peaks, _ = find_peaks(flux_s[a:b], height=np.percentile(flux_s, 70))
        return {
            "start": round(a / FPS, 1),
            "end": round(b / FPS, 1),
            "len": round((b - a) / FPS, 1),
            "energy_db": round(float(np.mean(rms_s[a:b])), 1),
            "centroid_hz": round(float(np.mean(centroid_s[a:b]))),
            "bass": round(float(np.mean(bass_s[a:b])), 3),
            "onsets_per_s": round(len(onset_peaks) / ((b - a) / FPS + 1e-9), 2),
        }

    segments = [seg_stats(a, b) for a, b in zip(bounds, bounds[1:])]
    bpm, strength = estimate_bpm(flux_s)

    return {"file": path, "duration": round(dur, 1), "bpm": bpm,
            "bpm_strength": strength, "segments": segments}


def fmt_ts(t: float) -> str:
    return f"{int(t // 60)}:{int(t % 60):02d}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--min-sec", type=float, default=12.0)
    ap.add_argument("--json", dest="json_out")
    args = ap.parse_args()

    result = analyze(args.audio, args.min_sec)
    if args.json_out:
        with open(args.json_out, "w") as fh:
            json.dump(result, fh, indent=2)

    print(f"File: {result['file']}  duration {fmt_ts(result['duration'])}  "
          f"BPM ~{result['bpm']} (strength {result['bpm_strength']})")
    print(f"{'#':>2} {'start':>6} {'end':>6} {'len':>5} {'dB':>6} {'cent':>6} {'bass':>5} {'ons/s':>5}")
    for i, s in enumerate(result["segments"]):
        print(f"{i:>2} {fmt_ts(s['start']):>6} {fmt_ts(s['end']):>6} "
              f"{s['len']:>5} {s['energy_db']:>6} {s['centroid_hz']:>6} "
              f"{s['bass']:>5} {s['onsets_per_s']:>5}")


if __name__ == "__main__":
    main()
