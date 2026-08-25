#!/usr/bin/env python3
"""Chunk the r4 canonical diff into 7 file-group chunks (<=~3000 lines each).

Deterministic: splits surge.t1 at the hunk boundary nearest the midpoint.
Same scheme as r3; r4 additions: tools/lint.sh -> c1, goldens/surge/149000ms.png -> c5.
"""
import os, sys

R4 = "/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r4"
DIFF = os.path.join(R4, "diff.patch")

CHUNK_OF = {}
CHUNK_OF["c1"] = [
    "_bmad-output/implementation-artifacts/spec-4-2-surge-crisis.md",
    "core/crisis_test.odin", "core/crisis.odin", "core/catalog.odin",
    "core/catalog_test.odin", "core/flow.odin", "core/types.odin",
    "core/serialize.odin", "core/step.odin", "core/determinism_test.odin",
    "core/warnings.odin", "app/render/crisis.odin", "app/main.odin",
    "app/render/view.odin", "harness/catalogs.odin", "harness/goldens.odin",
    "data/crises.json", "data/demand.json", "demos/surge.dem",
    "tools/lint.sh",
]
CHUNK_OF["c2"] = ["goldens/qos.t1", "goldens/qos/65000ms.png", "goldens/qos.log.bin"]
CHUNK_OF["c3"] = ["goldens/warn.t1", "goldens/warn/65000ms.png", "goldens/warn.log.bin"]
CHUNK_OF["c4"] = ["SURGE_A"]
CHUNK_OF["c5"] = ["SURGE_B", "goldens/surge/65000ms.png", "goldens/surge/30000ms.png",
                  "goldens/surge/170000ms.png", "goldens/surge/119500ms.png",
                  "goldens/surge/149000ms.png", "goldens/surge.log.bin"]
CHUNK_OF["c6"] = ["goldens/qos_emphasis.t1", "goldens/sla.t1",
                  "goldens/qos_contention.t1", "goldens/boot.t1"]
CHUNK_OF["c7"] = ["goldens/place.t1", "goldens/ecmp.t1", "goldens/demolish.t1",
                  "goldens/bundle.t1", "goldens/lose.t1", "goldens/win.t1",
                  "goldens/flow.t1", "goldens/draw.t1",
                  "goldens/win.log.bin", "goldens/place.log.bin",
                  "goldens/lose.log.bin", "goldens/flow.log.bin",
                  "goldens/ecmp.log.bin", "goldens/draw.log.bin",
                  "goldens/demolish.log.bin", "goldens/bundle.log.bin",
                  "goldens/boot.log.bin", "goldens/qos_emphasis.log.bin",
                  "goldens/sla.log.bin", "goldens/qos_contention.log.bin"]

with open(DIFF) as f:
    lines = f.read().splitlines(keepends=True)

blocks = {}
order = []
cur_file = None
cur_hdr = []
cur_hunks = []
cur_hunk = []
for ln in lines:
    if ln.startswith("diff --git"):
        if cur_file:
            cur_hunks.append(cur_hunk)
            blocks[cur_file] = (cur_hdr, cur_hunks)
            order.append(cur_file)
        cur_file = ln.split(" b/")[-1].strip()
        cur_hdr = [ln]
        cur_hunks = []
        cur_hunk = []
    elif ln.startswith("@@"):
        if cur_hunk:
            cur_hunks.append(cur_hunk)
            cur_hunk = []
        cur_hunk.append(ln)
    else:
        if cur_file:
            cur_hunk.append(ln)
if cur_file:
    cur_hunks.append(cur_hunk)
    blocks[cur_file] = (cur_hdr, cur_hunks)
    order.append(cur_file)

def chunk_of_file(fpath):
    for cid, files in CHUNK_OF.items():
        if fpath in files:
            return cid
    return None

surge_hunks = blocks["goldens/surge.t1"][1]
body = []
hunk_hdr = None
for h in surge_hunks:
    for ln in h:
        if ln.startswith("@@"):
            hunk_hdr = ln
        else:
            body.append(ln)
mid = len(body) // 2
surge_a = ([hunk_hdr] if hunk_hdr else []) + body[:mid]
surge_b = ([hunk_hdr] if hunk_hdr else []) + body[mid:]
surge_hdr = blocks["goldens/surge.t1"][0]
print(f"surge split: a={len(surge_a)} b={len(surge_b)} (body {len(body)})")

out = {c: [] for c in CHUNK_OF}
for fpath in order:
    if fpath == "goldens/surge.t1":
        continue
    cid = chunk_of_file(fpath)
    if cid is None:
        print("UNASSIGNED:", fpath, file=sys.stderr)
        continue
    hdr, hunks = blocks[fpath]
    out[cid].extend(hdr)
    for h in hunks:
        out[cid].extend(h)

out["c4"].extend(surge_hdr)
out["c4"].extend(surge_a)
out["c5"].extend(surge_hdr)
out["c5"].extend(surge_b)

tot = 0
for cid in ["c1", "c2", "c3", "c4", "c5", "c6", "c7"]:
    p = os.path.join(R4, f"chunk-{cid}.patch")
    with open(p, "w") as f:
        f.writelines(out[cid])
    n = len(out[cid])
    tot += n
    print(f"{cid}: {n} lines")
print("total:", tot, "(canonical diff lines:", len(lines), ")")
