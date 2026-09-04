#!/usr/bin/env python3
"""Perkins r1 consolidation — verify statuses are merged in manually after re-verification.
This script: loads all lens JSONs, dedupes on (lowercased_title, location),
merges sources, keeps highest severity. Rejected findings are filtered by
REJECTED list below (verified false/timing-artifact)."""
import json, glob, os, sys

OUT = '/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-arch-egress-migration/r1'

# Findings rejected at Perkins verification (with reasons) — these NEVER reach the report.
REJECT = [
    # (lens-substring, title-substring, reason)
    ('architecture', 'PERKINS-MUTATION-S3',
     'timing artifact - the lens read flow.odin during the round\'s own S3 mutation window; the final tree is clean (git status empty, suite green, mutation restored)'),
]

SEV_ORDER = {'note': 0, 'warning': 1, 'blocker': 2}

all_findings = []
failed_layers = []
files = sorted(glob.glob(f'{OUT}/*.json'))
for f in files:
    name = os.path.basename(f)[:-5]
    if name in ('consolidated',):
        continue
    try:
        arr = json.load(open(f))
        assert isinstance(arr, list)
    except Exception as e:
        failed_layers.append(name)
        print(f'INVALID JSON: {f}: {e}', file=sys.stderr)
        continue
    for x in arr:
        x['_lens_file'] = name
        all_findings.append(x)

# rejections
kept = []
rejected = []
for x in all_findings:
    rejected_flag = False
    for lens_sub, title_sub, reason in REJECT:
        if lens_sub in x.get('_lens_file','') and title_sub.lower() in x.get('title','').lower():
            rejected.append((x, reason))
            rejected_flag = True
            break
    if not rejected_flag:
        kept.append(x)

# dedupe on (lowercased_title, location) — normalized: collapse whitespace
def norm(s): return ' '.join((s or '').lower().split())
def key_of(x): return (norm(x.get('title',''))[:60], norm(x.get('location',''))[:60])

merged = {}
for x in kept:
    k = key_of(x)
    if k not in merged:
        y = dict(x)
        y['source'] = [x.get('source','?')]
        merged[k] = y
    else:
        y = merged[k]
        src = x.get('source','?')
        if src not in y['source']:
            y['source'].append(src)
        if SEV_ORDER.get(x.get('severity','note'),0) > SEV_ORDER.get(y.get('severity','note'),0):
            y['severity'] = x.get('severity')
        if x.get('detail','') and x['detail'] not in y.get('detail',''):
            y['detail'] = (y.get('detail','') + ' | ' + x['detail']).strip()

final = list(merged.values())
counts = {'blocker':0,'warning':0,'note':0}
for x in final:
    counts[x.get('severity','note')] += 1

print(f'total lens findings: {len(all_findings)}; rejected: {len(rejected)}; merged unique: {len(final)}')
print(f'failed layers: {failed_layers or "none"}')
print(f'buckets: {counts}')
print()
for sev in ('blocker','warning','note'):
    items = [x for x in final if x.get('severity')==sev]
    items.sort(key=lambda x: -len(x.get('source',[])))
    print(f'=== {sev.upper()} ({len(items)}) ===')
    for x in items:
        print(f"  [{','.join(x['source'])}] {x.get('title','')[:90]}")
        print(f"      loc: {x.get('location','')}")
    print()

with open(f'{OUT}/merged-raw.json','w') as f:
    json.dump({'findings': final, 'rejected': [{'finding': r[0], 'reason': r[1]} for r in rejected], 'failed_layers': failed_layers}, f, indent=1)
print('wrote merged-raw.json')
