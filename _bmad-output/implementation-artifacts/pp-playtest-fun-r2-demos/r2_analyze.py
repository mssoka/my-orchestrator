#!/usr/bin/env python3
"""pp-playtest-fun R2 — per-run evidence extraction from a v3 stats stream."""
import sys, csv, io

def analyze(path):
    meter = {}      # tick -> meter
    score = {}      # tick -> score
    cls = {}        # tick -> {class: (demand, delivered, dropped, loss, lat)}
    for line in open(path, encoding='utf-8', errors='replace'):
        if line.startswith('G,'):
            f = line.strip().split(',')
            t = int(f[1]); meter[t] = int(f[5]); score[t] = int(f[4])
        elif line.startswith('C,'):
            f = line.strip().split(',')
            t = int(f[1]); c = int(f[2])
            # demand, delivered, dropped, loss_pct, avg_lat, sla_lat, sla_loss
            cls.setdefault(t, {})[c] = tuple(int(float(x)) for x in f[3:10])
    ticks = sorted(meter)
    if not ticks:
        print(f"{path}: EMPTY"); return
    last = ticks[-1]

    def s(t): return t / 20.0  # ticks -> seconds (20 Hz)

    era3 = next((t for t, d in sorted(cls.items()) if 1 in d), None)
    dips = [t for t in ticks if meter[t] < 100]
    first_dip = dips[0] if dips else None
    trough_t = min(dips, key=lambda t: meter[t]) if dips else None
    trough = meter[trough_t] if trough_t is not None else 100
    death = next((t for t in ticks if meter[t] == 0), None)
    healed = None
    if trough < 100:
        after = [t for t in dips if t > trough_t]
        # healed = first tick after trough where meter returns to 100
        healed = next((t for t in ticks if t > trough_t and meter[t] == 100), None)
    # surge window: ticks 1200..3000 (60s..150s)
    win = [t for t in ticks if 1200 <= t <= 3000]
    won = last >= 3000 and meter.get(3000, 0) > 0
    drops_total = 0
    if cls:
        # dropped is per-tick class drops; sum per-tick across the whole run
        drops_total = sum(v[2] for per in cls.values() for v in per.values())
    # check whether dropped is cumulative
    cum = False
    st = sorted(cls)
    if len(st) > 2:
        c0 = cls[st[0]]
        if 0 in c0:
            vals = [cls[t].get(0, (0,0,0,0,0,0,0))[2] for t in st[:200]]
            cum = all(vals[i+1] >= vals[i] for i in range(len(vals)-1)) and any(v > 0 for v in vals)
    drop_stat = "(cum?) " if cum else ""
    lat_surge = [cls[t][1][6] for t in win if t in cls and 1 in cls[t] and cls[t][1][3] > 0]
    lat_surge_email = [cls[t][0][6] for t in win if t in cls and 0 in cls[t] and cls[t][0][3] > 0]
    print(f"== {path.split('/')[-1]} ==")
    print(f" ticks: {last} ({s(last):.1f}s)  era3(streaming) @ {era3} ({s(era3):.1f}s)" if era3 else f" ticks: {last}, NO streaming demand")
    print(f" meter: first_dip {first_dip} ({s(first_dip):.2f}s) trough {trough}@{trough_t} ({s(trough_t) if trough_t else 0:.2f}s) healed@{healed} ({s(healed):.2f}s)" if first_dip else " meter: never left 100")
    if healed and trough_t: print(f"   heal: trough {trough} @ {s(trough_t):.2f}s -> 100 @ {s(healed):.2f}s (+{s(healed)-s(trough_t):.2f}s)")
    print(f" DEATH: meter 0 @ tick {death} ({s(death):.2f}s)" if death else " no death (meter > 0 throughout)")
    print(f" outcome: {'WON (window completed, meter alive)' if won else 'lost/short'}   final score {score[last]} @ {last}")
    print(f" drops {drop_stat}total(sum per-tick): {drops_total}")
    if lat_surge: print(f" streaming lat in window: min {min(lat_surge)} max {max(lat_surge)} (tol 1200)")
    if lat_surge_email: print(f" email lat in window: min {min(lat_surge_email)} max {max(lat_surge_email)} (tol 2000)")
    # meter trace at 1s granularity for shape
    shape = [(t, meter[t]) for t in ticks if t % 40 == 0]
    print(" meter@2s:", ' '.join(f"{t}:{m}" for t, m in shape[::1] if True)[:600])
    print()

for p in sys.argv[1:]:
    analyze(p)
