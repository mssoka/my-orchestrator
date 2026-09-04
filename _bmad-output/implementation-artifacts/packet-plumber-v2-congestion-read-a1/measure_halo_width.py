#!/usr/bin/env python3
"""measure_halo_width.py — A1 evidence: congested-link halo width series.

For each frame PNG: find the widest contiguous run of CONGESTION-HALO blend
pixels along both axes; record (frame, class, max run h, max run v).
The blend colors are the draw's own math: raw_tier*0.57 + state*0.43 with
raw = pipe_steel (0,150,240), state = amber (242,181,68) / red (232,69,69).
These are far from every raw state color, so node rings / crisis outlines
(raw amber/red) never classify as halo.

Usage: measure_halo_width.py <frames_dir> <out_csv>
"""
import sys, os, glob, csv, re
from PIL import Image

STEEL = (0, 150, 240)
AMBER = (242, 181, 68)
RED = (232, 69, 69)

def blend(raw, state):
    return tuple(int(raw[i] * 0.57 + state[i] * 0.43) for i in range(3))

HALO = {
    "amber": blend(STEEL, AMBER),   # (104, 163, 165)
    "red": blend(STEEL, RED),       # (99, 115, 166)
}
TOL = 14  # per-channel; AA edges tighten the run by ~1px, never widen it

def classify_px(px):
    for name, (r, g, b) in HALO.items():
        if abs(px[0] - r) <= TOL and abs(px[1] - g) <= TOL and abs(px[2] - b) <= TOL:
            return name
    return None

def max_run(img, axis):
    """max contiguous halo run along the axis; returns (run, class)."""
    w, h = img.size
    px = img.load()
    best, best_cls = 0, ""
    if axis == "h":  # scan rows (horizontal links)
        lines = ((px[x, y] for x in range(w)) for y in range(0, h, 1))
    else:            # scan cols (vertical links)
        lines = ((px[x, y] for y in range(h)) for x in range(0, w, 1))
    for line in lines:
        cur, cls = 0, None
        for p in line:
            c = classify_px(p)
            if c:
                cur += 1
                cls = c
            else:
                if cur > best:
                    best, best_cls = cur, cls or ""
                cur = 0
                cls = None
        if cur > best:
            best, best_cls = cur, cls or ""
    return best, best_cls

def main():
    frames_dir, out_csv = sys.argv[1], sys.argv[2]
    frames = sorted(glob.glob(os.path.join(frames_dir, "*.png")))
    rows = []
    for f in frames:
        m = re.search(r"-(\d+)ms\.png$", os.path.basename(f))
        ms = int(m.group(1)) if m else -1
        img = Image.open(f).convert("RGB")
        rh, ch = max_run(img, "h")
        rv, cv = max_run(img, "v")
        cls = ch if rh >= rv else cv
        rows.append((ms, cls, rh, rv))
        print(f"{os.path.basename(f)}  class={cls:5s}  run_h={rh:3d}  run_v={rv:3d}")
    with open(out_csv, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["frame_ms", "class", "max_run_h", "max_run_v"])
        w.writerows(rows)
    print(f"wrote {out_csv} ({len(rows)} frames)")

if __name__ == "__main__":
    main()
