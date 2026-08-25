#!/usr/bin/env python3
"""Golden-drift analysis: v2 vs HEAD goldens.
Per changed golden: total diff pixels, ink_soft-swap pixels (old == (92,98,106)),
and connected-component bboxes of the remaining diff (the font/layout surface).
"""
import subprocess, sys, io, json
import numpy as np
from PIL import Image
from scipy import ndimage  # may not exist; fallback below

WT = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-font-overhaul-r1"
OLD_INKSOFT = np.array([92, 98, 106, 255], dtype=np.uint8)
NEW_INKSOFT = np.array([66, 72, 80, 255], dtype=np.uint8)

def load(ref, path):
    data = subprocess.run(["git", "-C", WT, "show", f"{ref}:{path}"],
                          capture_output=True, check=True).stdout
    return np.array(Image.open(io.BytesIO(data)).convert("RGBA"), dtype=np.uint8)

files = subprocess.run(
    ["git", "-C", WT, "diff", "--name-only", "v2...HEAD", "--", "goldens/"],
    capture_output=True, check=True, text=True).stdout.split()
files = [f for f in files if f.endswith(".png")]

report = []
for f in sorted(files):
    try:
        old, new = load("v2", f), load("HEAD", f)
    except subprocess.CalledProcessError:
        report.append({"file": f, "error": "missing in one ref"})
        continue
    if old.shape != new.shape:
        report.append({"file": f, "error": f"shape {old.shape} vs {new.shape}"})
        continue
    diffmask = np.any(old != new, axis=2)
    n_diff = int(diffmask.sum())
    if n_diff == 0:
        report.append({"file": f, "diff": 0})
        continue
    swap = diffmask & np.all(old == OLD_INKSOFT, axis=2) & np.all(new == NEW_INKSOFT, axis=2)
    other = diffmask & ~swap
    ys, xs = np.nonzero(diffmask)
    entry = {
        "file": f, "diff": n_diff,
        "ink_soft_swap": int(swap.sum()),
        "other": int(other.sum()),
        "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
    }
    # crude component analysis on 'other' (8-connectivity, via pure numpy flood on downsampled mask)
    om = other
    # row-profile: which y-rows carry 'other' pixels (text bands = tight row clusters)
    rows = np.nonzero(om.any(axis=1))[0]
    if len(rows):
        bands = []
        start = prev = rows[0]
        for r in rows[1:]:
            if r > prev + 2:
                bands.append([int(start), int(prev)])
                start = r
            prev = r
        bands.append([int(start), int(prev)])
        entry["other_row_bands"] = bands[:12]
        entry["other_band_heights"] = [b[1]-b[0]+1 for b in bands[:12]]
    report.append(entry)

print(json.dumps(report, indent=1))
