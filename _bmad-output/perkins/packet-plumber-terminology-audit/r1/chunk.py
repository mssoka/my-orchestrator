#!/usr/bin/env python3
"""Split diff.patch into Perkins lens chunks for packet-plumber-terminology-audit r1.

c1 = code (core/app/harness/demos/data/project-context.md)
c2 = docs (_bmad-output)
gXX = golden chunks <= ~3050 lines; big .t1 files split into fragments
     (each fragment gets a CHUNK NOTE header; the .log.bin stub rides the
     first fragment of its demo).
"""
import re, json, os

OUT = "/Users/moses/code/_bmad-output/perkins/packet-plumber-terminology-audit/r1"
CAP = 3180

# --- parse the diff into per-file records: (path, [lines]) ---
files = []
cur_path = None
cur = []
with open(f"{OUT}/diff.patch") as f:
    for line in f:
        if line.startswith("diff --git "):
            if cur_path:
                files.append((cur_path, cur))
            cur_path = line.split()[2][2:]  # strip a/
            cur = [line]
        else:
            cur.append(line)
if cur_path:
    files.append((cur_path, cur))

code_dirs = ("core/", "app/", "harness/", "demos/", "data/")
c1, c2, goldens = [], [], []
for path, lines in files:
    if path.startswith("goldens/"):
        goldens.append((path, lines))
    elif path.startswith(code_dirs) or path == "project-context.md":
        c1.append((path, lines))
    elif path.startswith("_bmad-output/"):
        c2.append((path, lines))
    else:
        raise SystemExit(f"unclassified: {path}")

def write_chunk(name, records):
    body = []
    for p, ls in records:
        body.extend(ls)
    with open(f"{OUT}/{name}.patch", "w") as f:
        f.writelines(body)
    return len(body)

manifest = []
n = write_chunk("c1", c1)
manifest.append(("c1", n, len(c1), "code: " + ", ".join(p for p, _ in c1)))
n = write_chunk("c2", c2)
manifest.append(("c2", n, len(c2), "docs: " + ", ".join(p for p, _ in c2)))

# --- goldens: group per-demo (.t1 + .log.bin), split big ones ---
demos = {}
for p, ls in goldens:
    base = p[len("goldens/"):]
    demo = re.sub(r"\.(t1|log\.bin)$", "", base)
    demos.setdefault(demo, {})["t1" if base.endswith(".t1") else "bin"] = (p, ls)

def frag_split(demo, t1rec, binrec):
    """Split a big .t1 diff into <=CAP fragments with CHUNK NOTEs. Returns list of records-lists."""
    p, ls = t1rec
    # header lines: everything up to the first @@ hunk
    i = next(i for i, l in enumerate(ls) if l.startswith("@@"))
    header, body = ls[:i], ls[i:]
    if len(ls) <= CAP:
        recs = [(p, ls)]
        if binrec: recs.append(binrec)
        return [recs]
    # fragment the body
    frags = []
    room = CAP - len(header) - 8  # reserve for NOTE
    cur, cur_n = [], 0
    for l in body:
        if cur_n >= room:
            frags.append(cur); cur, cur_n = [], 0
        cur.append(l); cur_n += 1
    if cur: frags.append(cur)
    out = []
    total = len(frags)
    for k, frag in enumerate(frags, 1):
        note = [f"@@ CHUNK NOTE @@ fragment {k} of {total} of {p} — the full-file diff ({len(ls)} lines) was split mid-hunk for review-size; hunk headers within are the ORIGINAL file's. Adjacent fragments cover adjacent line ranges; continuity across fragments is verified by Perkins mechanically.\n"]
        recs = [(p + f" [fragment {k}/{total}]", header + note + frag)]
        if k == 1 and binrec: recs.append(binrec)
        out.append(recs)
    return out

# build demo units (unsplit or fragmented)
units = []  # (demo, [records-lists per fragment])
for demo in sorted(demos):
    t1 = demos[demo].get("t1"); b = demos[demo].get("bin")
    if t1 is None and b is not None:
        units.append((demo, [[b]])); continue
    units.append((demo, frag_split(demo, t1, b)))

# first-fit decreasing-ish: keep original order, pack fragments into chunks
chunks = []  # list of (records-list, linecount)
cur, cur_n = [], 0
for demo, frags in units:
    for recs in frags:
        sz = sum(len(ls) for _, ls in recs)
        if cur_n + sz > CAP and cur:
            chunks.append((cur, cur_n)); cur, cur_n = [], 0
        cur.extend(recs); cur_n += sz
if cur: chunks.append((cur, cur_n))

for idx, (recs, n) in enumerate(chunks, 1):
    name = f"g{idx}"
    write_chunk(name, recs)
    demos_in = []
    for p, _ in recs:
        d = p[len("goldens/"):]
        demos_in.append(d)
    manifest.append((name, n, len(recs), "; ".join(demos_in)))

with open(f"{OUT}/chunk-manifest.json", "w") as f:
    json.dump([{"chunk": m[0], "lines": m[1], "files": m[2], "contents": m[3]} for m in manifest], f, indent=1)
for m in manifest:
    print(f"{m[0]:>4} {m[1]:>6} lines {m[2]:>3} files  {m[3][:110]}")
print("total chunks:", len(manifest))
