#!/usr/bin/env python3
"""Consolidate r1 lens findings into consolidated.json — verification pass applied."""
import json, os

ROUND = "/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-congestion-read-a1/r1"

def load(lens):
    p = os.path.join(ROUND, lens + ".json")
    if not os.path.exists(p):
        return None
    with open(p) as f:
        return json.load(f)

lenses = ["blind", "edge", "acceptance", "security", "architecture", "codebase", "tests"]
raw = {}
for l in lenses:
    d = load(l)
    raw[l] = d

# --- verification pass (Perkins, against the round worktree) -------------------
# Each entry: key = (lens, title-prefix) -> verification verdict + verifier note.
VERIFY = {
    ("edge", "Palcheck §8 routed legs"): ("confirmed", "Read harness/palcheck.odin §8 in the worktree: legs (a)/(b)/(c) are wrapped in `if testing_lvl_ok`; the (d)+(e) routed block indexes `state.crisis.pipe_congestion[ps8]` with NO guard. The resize above is also gated on testing_lvl_ok, so a premise failure leaves a short/zero slice and (d) panics — masking the summary."),
    ("security", "motion-strip zoom override is silently ignored"): ("confirmed", "harness/motion_strip.odin: `if zoom_override >= 1.0 && zoom_override <= 4.0 { strip_zoom = zoom_override }` — out-of-band falls through silently; the CLI caller validates first, so only non-CLI/future callers can hit the silent path."),
    ("architecture", "Camera zoom band 1.0..4.0 restated"): ("confirmed", "Literal band `z >= 1.0 && z <= 4.0` in harness/demo.odin:643, harness/main.odin:212, and the override guard in harness/motion_strip.odin:114 — while CAM_ZOOM_MIN :: 1.0 / CAM_ZOOM_MAX :: 4.0 exist in app/render/camera.odin and the harness already imports the render package (rnd.*)."),
    ("architecture", "palcheck §8 routed-branch legs"): ("confirmed", "Same mechanism as the edge lens's finding — merged."),
    ("architecture", "Halo blend restated"): ("confirmed", "The 0.57/0.43 blend literal appears in BOTH draw_bundles branches (view.odin ~1024-1028 and ~1101-1105); the diff unified only the width law behind congested_halo_width. Pre-existing duplication the diff had the seam to unify."),
    ("codebase", "look_l1_test feeds world-px band values"): ("confirmed", "Draw site: `band := link_width_capped(...) * v.scale` (view.odin:993) = SCREEN px into congested_halo_width(band_screen, scale). The test passes 3.5/4.5 (world px, per its own comment) with scale 1.4/2.0 — a units mislabel. Numerically insensitive at every pair (the floor dominates: 16.8/16.8/24 either reading; the scale-1.0 pair is exactly faithful), so the law pin itself holds; the comments' interpretation is wrong."),
    ("codebase", "palcheck section-8 end-cap leak scan"): ("confirmed", "capa8 = node_screen({4,12}) = the node CENTER; the halo's end-cap circle is DrawCircleV(a, w*0.5) at the node center (~12px radius at scale 2), drawn in the BUNDLES pass — draw_world draws nodes AFTER bundles, and the node sprite (≥ tile-sized at ACCESS z=2.0) covers the entire ±12px cap circle, so the ±floor_px vertical scan at the cap column can never see halo pixels. Vacuous by geometry. The section's load-bearing legs (mid-column leak, routed leak, stroke width, delete-the-bump) are live — the A1 gate itself was independently mutation-proven this round."),
    ("codebase", "Three section-8 continuation comments"): ("confirmed", "Visible in the diff and in the worktree: `// into a calm board's draw`, `// the same floored width`, and the resize-block continuation carry an extra tab vs sibling comments."),
    ("acceptance", "Doc-hygiene constraint met by substitution"): ("confirmed", "The spec's 'ONE line in the repo's LOOK-SPEC' is unmet literally: look-node-legibility/LOOK-SPEC.md is untracked in git (verified via the deferred-work entry + absence from the repo tree), so the PR cannot carry it. The amendment IS recorded on the tracked canon (view.odin LOOK §3 comment block) + deferred-work.md routes the mirror. Documented, routed substitution — note-grade."),
    ("acceptance", "Rung pairs feed world px"): ("confirmed", "Same defect as the codebase units finding — merged."),
    ("acceptance", "Palcheck §8 routed legs index pipe_congestion unguarded"): ("confirmed", "Same mechanism as the edge lens's finding — merged."),
    ("tests", "Motion-strip capture-altitude behavior"): ("confirmed", "grep across harness/*_test.odin + app/render/*_test.odin: zero references to apply_capture_zoom / zoom_override / strip_zoom. The demo-zoom transform predates the diff but the extraction + the new zoom= override validation (main.odin) ship with no automated coverage; the corpus only exercises the default path."),
    ("tests", "Routed-calm leg pins leak-only"): ("confirmed", "§8(e) checks n_routed_leak == 0 only; the inline (c) pins stroke width == band_px ±3 AND leaks. A routed calm draw at the WRONG (non-covenant) width with no halo pixels passes (e)."),
    ("tests", "Advisory test gate"): ("confirmed", "CONCERNS is consistent with the verified gaps: P0 (the A1 floor law) is heavily covered (unit law test + palcheck §8 ×5 legs + corpus + this round's independent mutation legs); the uncovered motion-strip override path is a P2 gap → CONCERNS, not FAIL."),
}

merged = {}
order = []
dedupe_done = set()
MERGE = {  # title-prefix -> canonical key that absorbs it
    ("architecture", "palcheck §8 routed-branch legs"): ("edge", "Palcheck §8 routed legs"),
    ("acceptance", "Palcheck §8 routed legs index pipe_congestion unguarded"): ("edge", "Palcheck §8 routed legs"),
    ("acceptance", "Rung pairs feed world px"): ("codebase", "look_l1_test feeds world-px band values"),
}

for lens in lenses:
    d = raw.get(lens)
    if d is None:
        continue
    for f in d:
        key = (lens, f["title"][:40])
        vkey = None
        for (vl, pref), verdict in VERIFY.items():
            if vl == lens and f["title"].startswith(pref[:30]):
                vkey = (vl, pref)
                break
        if vkey is None:
            vkey_absorb = MERGE.get((lens, f["title"][:56]))
            if vkey_absorb:
                continue  # absorbed into canonical finding below
            vkey_absorb2 = None
            for (vl, pref) in VERIFY:
                if f["title"].startswith(pref[:30]):
                    vkey_absorb2 = (vl, pref)
                    break
            if vkey_absorb2 and vkey_absorb2[0] != lens:
                continue
            vkey = vkey_absorb2
        verdict = VERIFY.get(vkey, ("unverifiable-speculative", "no verifier entry matched"))
        ck = (lens, f["title"][:56])
        absorb = MERGE.get(ck)
        ident = absorb if absorb else (lens, f["title"][:40])
        ident_key = ident[1][:30]
        if ident_key not in merged:
            merged[ident_key] = {
                "sources": [],
                "finding": f,
                "verification": verdict[0],
                "verifier_note": verdict[1],
            }
            order.append(ident_key)
        merged[ident_key]["sources"].append(lens)
        if verdict[0] == "confirmed":
            merged[ident_key]["verification"] = "confirmed"
            merged[ident_key]["verifier_note"] = verdict[1]

out = []
for k in order:
    m = merged[k]
    f = dict(m["finding"])
    f["source"] = sorted(set(m["sources"]))
    f["verification"] = m["verification"]
    f["verifier_note"] = m["verifier_note"]
    out.append(f)

# triage
def sev(f):
    return f["severity"]
blockers = [f for f in out if sev(f) == "blocker"]
warnings = [f for f in out if sev(f) == "warning"]
notes = [f for f in out if sev(f) == "note"]

# demote unverifiable blockers per skill 3b.3
for f in out:
    if f["verification"] == "unverifiable-speculative" and f["severity"] == "blocker":
        f["severity"] = "warning"
        f["title"] = "[unverified] " + f["title"]
        blockers.remove(f)
        warnings.append(f)

result = {
    "round": "packet-plumber-v2-congestion-read-a1-perkins-r1",
    "reviewed_sha": "df147854ff24be3a73437120b5fdeeeb482318af",
    "diff_file": os.path.join(ROUND, "diff.patch"),
    "spec_files": [
        "/Users/moses/code/_bmad-output/briefs/packet-plumber-v2-congestion-read-a1.md",
        "/Users/moses/code/_bmad-output/implementation-artifacts/packet-plumber-v2-viscomm-regression-audit/viscomm-regression-audit.md",
    ],
    "lenses_completed": sorted([l for l in lenses if raw.get(l) is not None]),
    "lenses_failed": sorted([l for l in lenses if raw.get(l) is None]),
    "raw_findings": sum(len(v) for v in raw.values() if v),
    "verified_confirmed": sum(1 for f in out if f["verification"] == "confirmed"),
    "rejected": 0,
    "unverifiable_kept": sum(1 for f in out if f["verification"] == "unverifiable-speculative"),
    "blockers": len(blockers),
    "warnings": len(warnings),
    "notes": len(notes),
    "findings": out,
    "perkins_verification_pass": {
        "unit_tests": "app/render 116/116 GREEN (incl. the 2 new A1 pin tests); app 51/51; core 280/280",
        "palcheck": "all green incl. new §8 (amber/red/routed floor legs 24px; calm stroke 10px ≈ band 9, halo leak 0, routed calm leak 0; non-vacuous premise: floor dominates bump 19<21)",
        "mutation_leg_delete_the_bump": "RED: congested_halo_width floor deleted → unit law test fails ×6 (8.5/10.5/14.5/11/19 under floor; 14.5≠24) + palcheck §8 (a)/(b)/(d) FAIL at exactly the predicted 19px-vs-24; GREEN: restored → 116/116 + palcheck all green; worktree byte-identical to reviewed sha after restore",
        "calm_covenant": "§8(c)/(e) leak legs green in BOTH mutation states; corpus 49/49 (T1+T2+replay byte-exact — every un-re-blessed golden byte-identical, ODN-1 sim/log untouched)",
        "corpus": "49/49 demos green",
        "motion_strip_series": "CSV-verified 50/50 frames per rung: warn z1.0 8→12px, z1.4 10→16px, z2.0 18→22px (matches claims); juice after oscillates 7↔14 (live telegraph) where before was static 7",
        "golden_pixel_diffs": "re-blessed PNGs vs base 03dd6f8: juice@65s 683px, warn@45s 1103px (one 279×12 link band), qos_contention@1s 2110px, surge@65s 269px, pause@65s 265px, a11y_reduced@65s 342px, juice@30s 422px — ALL confined to thin link-corridor bands = the A1 emphasis layer only; no HUD/node/full-frame churn",
    },
}

with open(os.path.join(ROUND, "consolidated.json"), "w") as f:
    json.dump(result, f, indent=1)
print("lenses completed:", result["lenses_completed"])
print("lenses failed:", result["lenses_failed"])
print(f"raw {result['raw_findings']} → confirmed {result['verified_confirmed']}, rejected {result['rejected']}, unverifiable {result['unverifiable_kept']}")
print(f"B {result['blockers']} / W {result['warnings']} / N {result['notes']}")
for f in out:
    print(f" [{f['severity']}] {f['source']} {f['title'][:80]}")
