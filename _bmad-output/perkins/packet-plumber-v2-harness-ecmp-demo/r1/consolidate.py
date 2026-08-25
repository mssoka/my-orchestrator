#!/usr/bin/env python3
"""Write consolidated.json for packet-plumber-v2-harness-ecmp-demo r1 (single wave, 7 lenses).
Run AFTER the lens JSONs exist and AFTER Perkins has verified each finding against the worktree."""
import json, sys

OUT = "/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-harness-ecmp-demo/r1"
LENSES = ["blind", "edge", "acceptance", "security", "architecture", "codebase", "tests"]

# 1. Load raw lens outputs
raw = {}
total = 0
for lens in LENSES:
    try:
        with open(f"{OUT}/{lens}.json") as f:
            data = json.load(f)
        assert isinstance(data, list), f"{lens}.json not a list"
        raw[lens] = data
        total += len(data)
    except FileNotFoundError:
        print(f"MISSING {lens}.json")
        sys.exit(1)
print("raw findings per lens:", {k: len(v) for k, v in raw.items()}, "total", total)

# 2. The verified consolidated findings (Perkins wrote this block by hand after
#    verifying every raw finding against the worktree). Edit me.
F = []
def f(sources, severity, category, title, location, evidence, detail, fix, verification):
    F.append({"sources": sources, "severity": severity, "category": category, "title": title,
              "location": location, "evidence": evidence, "detail": detail,
              "recommended_fix": fix, "verification": verification})

# <-- Perkins: append f(...) entries here (post-verification, deduped) -->

counts = {"blocker": 0, "warning": 0, "note": 0}
for x in F:
    counts[x["severity"]] += 1
n_blockers = counts["blocker"]
verdict = "READY TO MERGE" if n_blockers == 0 else ("NEEDS CHANGES" if n_blockers <= 3 else "MAJOR REWORK NEEDED")

out = {
    "job": "packet-plumber-v2-harness-ecmp-demo",
    "round": 1,
    "pr": 29,
    "reviewed_sha": "f90351da1054d2b213ceb1a22afedc7e718c3d38",
    "diff_file": f"{OUT}/diff.patch",
    "chunking": "diff 663 lines <= ~3000 => single wave, 7 lenses, no chunking",
    "worktree": "/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-harness-ecmp-demo-r1",
    "reviewers_completed": 7,
    "reviewers_total": 7,
    "failed_layers": [],
    "total_findings": total,
    "unique_after_dedupe": len(F),
    "verified_confirmed": sum(1 for x in F if x["verification"] == "confirmed"),
    "rejected": 0,
    "unverifiable_speculative": sum(1 for x in F if x["verification"] == "unverifiable-speculative"),
    "counts": counts,
    "verdict": verdict,
    "verdict_reason": "",
    "findings": F,
}
with open(f"{OUT}/consolidated.json", "w") as fh:
    json.dump(out, fh, indent=1)
print("wrote consolidated.json:", verdict, counts)
