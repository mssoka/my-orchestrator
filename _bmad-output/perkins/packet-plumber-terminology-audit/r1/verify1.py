#!/usr/bin/env python3
"""Perkins r1 verification pass 1 — mechanical evidence location check.
For every raw finding: resolve location against the worktree / diff, check the
evidence quote verbatim. Emits verify-report.json + a triage summary."""
import json, glob, re, os

R = "/Users/moses/code/_bmad-output/perkins/packet-plumber-terminology-audit/r1"
WT = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-pp-terminology-audit-r1"
diff = open(f"{R}/diff.patch").read()

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

ndiff = norm(diff)

def evidence_locatable(ev):
    """Return True if any substantive line of the evidence appears in worktree files or the diff."""
    if not ev or ev.strip() in ("N/A", "n/a"): return None  # unanchored
    # split evidence into candidate lines; try longest first
    lines = [l.strip() for l in ev.split("\n") if len(l.strip()) > 12]
    if not lines:
        lines = [l for l in ev.split(";") if len(l.strip()) > 12]
    if not lines: return None
    hits = 0
    for l in lines[:6]:
        nl = norm(l).strip('`')
        if not nl: continue
        if nl in ndiff:
            hits += 1; continue
        # search worktree text files
        found = False
        for root, dirs, files in os.walk(WT):
            dirs[:] = [d for d in dirs if d not in (".git","bin","raylib-sw","node_modules")]
            for fn in files:
                if fn.endswith((".odin",".md",".json",".dem",".t1",".sh")):
                    try:
                        if nl in norm(open(os.path.join(root,fn),errors="ignore").read()):
                            found = True; break
                    except Exception: pass
            if found: break
        if found: hits += 1
    return hits > 0

report = []
for f in sorted(glob.glob(f"{R}/*.json")):
    base = os.path.basename(f)[:-5]
    parts = base.split("-")
    if len(parts) < 2 or parts[0] not in ("blind","edge","acceptance","security","architecture","codebase","tests"): continue
    lens, chunk = parts[0], parts[-1]
    try: d = json.load(open(f))
    except: continue
    for i, x in enumerate(d):
        ev = x.get("evidence","")
        loc = evidence_locatable(ev)
        report.append({
            "id": f"{lens}-{chunk}#{i}", "lens": lens, "chunk": chunk,
            "severity": x.get("severity"), "category": x.get("category"),
            "title": x.get("title"), "location": x.get("location"),
            "mech": "unanchored" if loc is None else ("locatable" if loc else "NOT-FOUND"),
            "finding": x,
        })

json.dump(report, open(f"{R}/verify-report.json","w"), indent=1)
import collections
c = collections.Counter(r["mech"] for r in report)
print("mechanical verdicts:", dict(c))
bysev = collections.Counter((r["severity"], r["mech"]) for r in report)
for k in sorted(bysev): print(k, bysev[k])
