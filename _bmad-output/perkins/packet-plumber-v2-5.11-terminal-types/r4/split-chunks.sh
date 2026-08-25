#!/bin/bash
# split-chunks.sh — partition the canonical r4 diff into lens chunks
# code : all non-golden files (the whole delta + settled code)
# g1   : fold-critical + new goldens (boot, node_health, terminal_types, input-parity, binaries)
# g2   : 8 big .t1 as head/tail excerpts (identical bytes to r3's whole-file waves — git-proven)
# g3-g5: remaining .t1 whole, greedily packed <=2950 diff lines
set -euo pipefail
R4=/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r4
cd "$R4"
mkdir -p chunks
python3 - <<'EOF'
import re, subprocess, sys

diff = open('/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r4/diff.patch').read()
# split into per-file segments (headers start with 'diff --git ')
parts = re.split(r'(?m)^(?=diff --git )', diff)
parts = [p for p in parts if p.strip()]
files = []
for p in parts:
    m = re.match(r'diff --git a/(\S+) b/(\S+)', p)
    files.append((m.group(2), p))

def lines(s): return s.count('\n')

code_files = [(f,p) for f,p in files if not f.startswith('goldens/')]
golden_files = [(f,p) for f,p in files if f.startswith('goldens/')]

# g1 forced set
g1_names = {'goldens/boot.t1','goldens/node_health.t1','goldens/terminal_types.t1',
            'goldens/input_parity_draw.t1','goldens/input_parity_draw_wide.t1'}
# binaries + pngs auto-include in g1
g1, rest = [], []
for f,p in golden_files:
    if f in g1_names or not f.endswith('.t1'):
        g1.append((f,p))
    else:
        rest.append((f,p))

# g2: the 8 big files (>2000 diff lines) as head/tail excerpts
big, small = [], []
for f,p in rest:
    (big if lines(p) > 2000 else small).append((f,p))

def excerpt(f, p, head=250, tail=100):
    out = []
    ls = p.split('\n')
    # keep the file header (diff/index/---/+++) = lines until first @@
    i = 0
    while i < len(ls) and not ls[i].startswith('@@'):
        out.append(ls[i]); i += 1
    body = ls[i:]
    # body lines: keep context/add/del; note removals shrink what 'tail' sees — fine for orientation
    h = body[:head]
    t = body[-tail:]
    elided = len(body) - head - tail
    out += h
    out.append(f'... [{elided} lines elided from this golden\'s diff body — the FULL file is in the review worktree at {f}; read it there if needed] ...')
    out += t
    return '\n'.join(out) + '\n', len(out)

g2, g2_meta = [], []
for f,p in big:
    e, n = excerpt(f,p)
    g2.append((f,e)); g2_meta.append((f,n))

# g3-g5: greedy pack the small whole files <=2950
small.sort(key=lambda fp: -lines(fp[1]))
bins, bin_sizes = [], []
for f,p in small:
    n = lines(p)
    placed = False
    for i in range(len(bins)):
        if bin_sizes[i] + n <= 2950:
            bins[i].append((f,p)); bin_sizes[i] += n; placed=True; break
    if not placed:
        bins.append([(f,p)]); bin_sizes.append(n)

def write(name, flist):
    with open(f'/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r4/chunks/{name}.diff','w') as fh:
        for f,p in flist:
            fh.write(p if p.endswith('\n') else p+'\n')
    total = sum(lines(p) for f,p in flist)
    print(f'{name}: {len(flist)} files, {total} diff lines')
    return total

write('code', code_files)
write('g1', g1)
write('g2', g2)
names = ['g3','g4','g5','g6'][:len(bins)]
for nm, b in zip(names, bins):
    write(nm, b)
# manifest
with open('/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r4/chunks/MANIFEST.txt','w') as fh:
    fh.write('code: '+', '.join(f for f,_ in code_files)+'\n\n')
    fh.write('g1: '+', '.join(f for f,_ in g1)+'\n\n')
    fh.write('g2 (excerpts): '+', '.join(f'{f}({n})' for (f,_),n in zip(g2,g2_meta))+'\n\n')
    for nm,b in zip(names,bins):
        fh.write(nm+': '+', '.join(f for f,_ in b)+'\n\n')
covered = sum(lines(p) for _,p in code_files+g1+small) + sum(n for _,n in g2_meta)
print(f'total covered (excerpted): {covered} of {lines(diff)} canonical lines')
EOF
