#!/usr/bin/env python3
"""measure_halo_pulse.py — A1-as-amended evidence: congested-link pulse
INTENSITY series (state-color share over time, NOT width — sizes unchanged).

For each frame PNG: within the analysis window (fit coords, scaled by the
strip zoom), collect pixels that sit within TOL of the raw->state color
SEGMENT (steel -> amber or steel -> red; the draw's blend line at any pulse
share), and report the MEAN projected share s where
P = raw*(1-s) + state*s  =>  s = P.r / state.r  (raw.r == 0).

A flat series at ~0.43 = no pulse (the A1/pre-A1 recolor); an oscillating
series sweeping toward ~0.75 = the pulse (PULSE16, 16-tick cycle = 1.25 Hz).

Usage: measure_halo_pulse.py <frames_dir> <out_csv> <zoom>
"""
import sys, os, glob, csv, re
from PIL import Image

RAW = (0, 150, 240)          # pipe_steel
STATES = {"amber": (242, 181, 68), "red": (232, 69, 69)}
TOL = 14
# the warn demo's congested corridor, FIT coordinates (the T2 diff bbox band)
FIT_WIN = (650, 348, 915, 372)  # x0, y0, x1, y1 (inclusive-ish)
FIT_CENTER = (640.0, 360.0)     # the fit view centers the world in the window

def on_segment(p, state):
    """share s if p sits within TOL of the raw->state segment, else None."""
    num = p[0] - RAW[0]
    den = state[0] - RAW[0]
    if den == 0:
        return None
    s = num / den
    if s < 0.35 or s > 0.95:   # the pulse sweeps 0.43..0.75; AA edges excluded
        return None
    c = tuple(RAW[i] * (1 - s) + state[i] * s for i in range(3))
    if abs(p[0] - c[0]) <= TOL and abs(p[1] - c[1]) <= TOL and abs(p[2] - c[2]) <= TOL:
        return s
    return None

def mean_share(img, zoom):
    """mean + max share over on-segment pixels: mean = the corridor's blend,
    max = the GLOW envelope top (the split render keeps the core at the
    trough share, so the max tracks the oscillation undamped)."""
    px = img.load()
    cx, cy = FIT_CENTER
    x0 = int(cx + (FIT_WIN[0] - cx) * zoom)
    y0 = int(cy + (FIT_WIN[1] - cy) * zoom)
    x1 = int(cx + (FIT_WIN[2] - cx) * zoom)
    y1 = int(cy + (FIT_WIN[3] - cy) * zoom)
    tot, n, mx = 0.0, 0, None
    for y in range(max(0, y0), min(img.size[1], y1 + 1)):
        for x in range(max(0, x0), min(img.size[0], x1 + 1)):
            p = px[x, y]
            for st in STATES.values():
                s = on_segment(p, st)
                if s is not None:
                    tot += s
                    n += 1
                    if mx is None or s > mx:
                        mx = s
                    break
    mean = (tot / n) if n else None
    return mean, (mx if n else None), n

def main():
    frames_dir, out_csv, zoom_s = sys.argv[1], sys.argv[2], float(sys.argv[3])
    rows = []
    for f in sorted(glob.glob(os.path.join(frames_dir, "*.png"))):
        m = re.search(r"-(\d+)ms\.png$", os.path.basename(f))
        ms = int(m.group(1)) if m else -1
        img = Image.open(f).convert("RGB")
        s, mx, n = mean_share(img, zoom_s)
        rows.append((ms, s, mx, n))
        print(f"{os.path.basename(f)}  mean={'--' if s is None else f'{s:.3f}'}  max={'--' if mx is None else f'{mx:.3f}'}  px={n}")
    with open(out_csv, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["frame_ms", "mean_state_share", "max_state_share", "pixels"])
        w.writerows(rows)
    vals = [r[2] for r in rows if r[2] is not None]
    means = [r[1] for r in rows if r[1] is not None]
    if vals:
        print(f"wrote {out_csv}: MAX(glow envelope) {min(vals):.3f}..{max(vals):.3f} span={max(vals)-min(vals):.3f} | MEAN {min(means):.3f}..{max(means):.3f} over {len(vals)} frames")

if __name__ == "__main__":
    main()
