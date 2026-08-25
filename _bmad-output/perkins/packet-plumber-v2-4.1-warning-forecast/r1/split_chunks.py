#!/usr/bin/env python3
"""Split the canonical diff.patch into per-chunk patches for the lens waves (r1)."""
import re, os

OUT = "/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.1-warning-forecast/r1"
patch = open(f"{OUT}/diff.patch").read()

files = re.split(r'(?=^diff --git )', patch, flags=re.M)
by_name = {}
for f in files:
    m = re.match(r'diff --git a/(\S+) b/\S+', f)
    if not m:
        continue
    by_name[m.group(1)] = f

chunks = {
    "c1": [
        "_bmad-output/implementation-artifacts/epic-4-context.md",
        "_bmad-output/implementation-artifacts/spec-4-1-warning-forecast.md",
        "app/main.odin",
        "app/render/forecast.odin",
        "app/render/palette.odin",
        "app/render/view.odin",
        "core/catalog.odin",
        "core/catalog_test.odin",
        "core/determinism_test.odin",
        "core/flow.odin",
        "core/qos_test.odin",
        "core/serialize.odin",
        "core/step.odin",
        "core/types.odin",
        "core/warnings.odin",
        "core/warnings_test.odin",
        "data/balance.json",
        "demos/lose.dem",
        "demos/warn.dem",
        "harness/goldens.odin",
        "harness/run.odin",
    ],
    "c2": [
        "goldens/warn.log.bin",
        "goldens/warn.t1",
        "goldens/warn/01500ms.png",
        "goldens/warn/45000ms.png",
        "goldens/warn/65000ms.png",
    ],
    "c3": [
        "goldens/qos.log.bin",
        "goldens/qos.t1",
        "goldens/qos/01000ms.png",
        "goldens/qos/65000ms.png",
    ],
    "c4": [
        "goldens/boot.log.bin", "goldens/boot.t1",
        "goldens/bundle.log.bin", "goldens/bundle.t1",
        "goldens/demolish.log.bin", "goldens/demolish.t1",
        "goldens/draw.log.bin", "goldens/draw.t1",
        "goldens/ecmp.log.bin", "goldens/ecmp.t1",
        "goldens/flow.log.bin", "goldens/flow.t1",
        "goldens/lose.log.bin", "goldens/lose.t1", "goldens/lose/03000ms.png",
        "goldens/place.log.bin", "goldens/place.t1",
        "goldens/win.log.bin", "goldens/win.t1",
    ],
    "c5": [
        "goldens/qos_contention.log.bin", "goldens/qos_contention.t1",
        "goldens/qos_contention/01000ms.png", "goldens/qos_contention/03000ms.png",
        "goldens/qos_contention/10000ms.png",
        "goldens/qos_emphasis.log.bin", "goldens/qos_emphasis.t1",
        "goldens/qos_emphasis/01000ms.png", "goldens/qos_emphasis/05000ms.png",
        "goldens/qos_emphasis/12000ms.png",
        "goldens/sla.log.bin", "goldens/sla.t1",
        "goldens/sla/01000ms.png", "goldens/sla/04000ms.png",
    ],
}

missing = []
for cname, names in chunks.items():
    parts = []
    for n in names:
        if n not in by_name:
            missing.append(n)
            continue
        parts.append(by_name[n])
    blob = "".join(parts)
    with open(f"{OUT}/{cname}.patch", "w") as f:
        f.write(blob)
    nlines = blob.count("\n")
    print(f"{cname}: {len(names)} files, {nlines} lines -> {OUT}/{cname}.patch")
if missing:
    print("MISSING:", missing)
else:
    print("all files accounted for")
