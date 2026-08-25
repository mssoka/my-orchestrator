#!/usr/bin/env python3
"""Build consolidated.json for Perkins r1 — terminology-audit PR #55."""
import json, glob

R = "/Users/moses/code/_bmad-output/perkins/packet-plumber-terminology-audit/r1"

# cluster assignment (same logic as the review pass)
CLUSTERS = {
 "W1": ["STRAINED"],
 "W2": ["contradicts itself", "contradicts", "Gate-2", "still OPEN"],
 "N10": ["validate_set_emphasis", "apply_set_emphasis", "press`", "press var", "press local"],
 "N1": ["qos_manual", "qos_auto"],
 "N2": ["demand.json"],
 "N3": ["congestion-plan"],
 "N4": ["ladder"],
 "N5": ["time congestion", "modernization congestion", "congestion-riser", "idiom", "Everyday-English", "ordinary-English", "sustained congestion", "fair congestion"],
 "N6": ["Strain metrics", "full ladder", "stories-v2"],
 "N7": ["ASCII", "borders", "box"],
 "N8": ["congested/congested", "as a verb", "duplicated noun", "grammar wart", "Grammar wart", "noun-as-verb", "verb"],
 "N9": ["Set_Emphasis", "Strain measure", "priority-emphasis dial", "epics", "ODN-12"],
 "GATE": ["Advisory test gate"],
}
# unclustered-id -> cluster (or "REJECT")
MANUAL = {
 "architecture-c2#0": "N8", "blind-c2#1": "N8", "tests-c2#6": "N8",
 "architecture-g1#2": "REJECT-historical", "architecture-g11#1": "REJECT-historical",
 "architecture-g13#1": "REJECT-historical", "architecture-g14#1": "REJECT-historical",
 "codebase-c2#3": "REJECT-historical", "codebase-g11#1": "REJECT-historical",
 "codebase-g2#4": "REJECT-historical", "codebase-g3#5": "REJECT-historical",
 "codebase-g4#3": "REJECT-historical", "security-g1#1": "REJECT-historical",
 "architecture-g1#6": "REJECT-out-of-scope",
 "edge-c1#1": "REJECT-backcompat", "architecture-g13#3": "REJECT-backcompat", "tests-c2#3": "REJECT-backcompat",
 "architecture-g1#3": "N10", "tests-c1#1": "N10", "architecture-g6#4": "N10",
 "architecture-g13#4": "N9", "codebase-c2#4": "N9", "codebase-g13#3": "N9",
 "codebase-c2#5": "N9", "codebase-c2#9": "N9",
 "security-c2#2": "REJECT-misread",
 "tests-c1#9": "GATE",
}

members = {k: [] for k in list(CLUSTERS)+["REJECT-historical","REJECT-out-of-scope","REJECT-backcompat","REJECT-misread"]}
for f in sorted(glob.glob(f"{R}/*.json")):
    base = f[len(R)+1:-5]
    parts = base.split("-")
    if len(parts) < 2 or parts[0] not in ("blind","edge","acceptance","security","architecture","codebase","tests"): continue
    lens, chunk = parts[0], parts[-1]
    try: d = json.load(open(f))
    except: continue
    for i, x in enumerate(d):
        fid = f"{lens}-{chunk}#{i}"
        t = (x.get("title","")+" "+x.get("detail","")+" "+x.get("location",""))
        cid = MANUAL.get(fid)
        if cid is None:
            for c, keys in CLUSTERS.items():
                if any(k in t for k in keys): cid = c; break
        if cid is None: cid = "UNASSIGNED"
        members.setdefault(cid, []).append((lens, chunk, x))

def srclist(v): return sorted(set(l for l, _, _ in v))

def mk(cid, severity, category, title, location, evidence, detail, fix):
    v = members[cid]
    return {"sources": srclist(v), "severity": severity, "category": category, "title": title,
            "location": location, "evidence": evidence, "detail": detail, "recommended_fix": fix,
            "verification": "confirmed", "lens_filings": len(v)}

warnings = [
 mk("W1", "warning", "rename-completeness",
    "Player-facing node-health inspect card still renders \"STRAINED\" — a rendered strain-coinage string absent from the audit's rendered-strings inventory (the fold-or-keep listing rule has a hole)",
    "app/render/node_health.odin:25",
    "`if lvl == .Amber { return \"STRAINED\", p.state_congested, \"!\" }` — the PR renamed the type (Congestion_Level) and the palette field (state_congested) on this very line but left the rendered label",
    "The audit's 'Rendered HUD strings carrying coinage' table lists 6 strings; this 7th was never inventoried, so the PR neither folded it nor listed it as kept. Hover-only (the harness never renders the card — zero T2 impact either way).",
    "Decide + list: rename to \"CONGESTED\" as a deliberate listed fold (no T2 impact — the card is app-hover only), or record an explicit keep in the PR body."),
 mk("W2", "warning", "record-integrity",
    "The audit record §4 contradicts itself and this PR's canon entry on Phase-2 status and the 5.2 merge",
    "_bmad-output/implementation-artifacts/terminology-audit-v1.md:112-118",
    ":112 `## 4. Phase 2 scope (NOT started — verdict cleared, 5.2 gate remains)` + :117 `- **Gate 2 — 5.2's merge (still OPEN):** v2-5.2-node-health is NOT merged to v2 as of 2026-08-15` vs :114 `**Phase 2 shipped 2026-08-15** (PR #55)` and decision-log.md `Phase-2 rename PR serialized behind 5.2's merge (merged 2026-08-15, PR #54 …)`",
    "The shipped audit record (this PR's own evidence trail) carries a stale heading + Gate-2 bullet amended only in its Gate-1 line — future readers (and r2) read two contradictory states.",
    "Amend §4's heading + Gate-2 bullet to the shipped state (5.2 merged PR #54; Phase 2 = this PR)."),
]

notes = [
 mk("N1", "note", "sweep-residue", "Live demo comments still name Cmd_Set_Emphasis (ruled → Cmd_Set_Weights)", "demos/qos_manual.dem:4; demos/qos_auto.dem:7",
    "qos_manual.dem:4 '# the SAME serialized command as the auto ladder (Cmd_Set_Emphasis weights;' · qos_auto.dem:7 '# computed set through Cmd_Set_Emphasis (the `weights` directive pins the)'",
    "Comment-only (the parser strips them; zero sim/golden impact); the sweep simply didn't visit these two files.", "Rename the two comment references."),
 mk("N2", "note", "sweep-residue", "data/demand.json _comment still cites scripted_plan_pressure (ruled → scripted_plan_demand)", "data/demand.json:2",
    "`Story 3.1: scripted_plan_pressure returns the active era's entries …`", "A live catalog _comment string naming a symbol that no longer exists. NOTE the fold: demand.json bytes fold into catalog_hash, so fixing it re-blesses every golden — bundle the fix with the next data-touching PR.",
    "Rename in the next catalog-touching PR (absorbs the re-bless), or accept as a documented residue."),
 mk("N3", "note", "mis-rename", "\"pressure-plan director\" became \"congestion-plan director\" — the canon maps Pressure_Plan → Demand_Plan, not → congestion", "core/flow.odin:51; harness/demo.odin:28",
    "flow.odin:51 `The congestion-plan director (weighted src/dst picks) is the real demand model (3.1)` · demo.odin:28 `The congestion-plan director (weighted picks) lands in slice 3.`",
    "The mechanical pressure→congestion substitution hit the demand-director gloss, conflating the plan with congestion; both sentences describe the DEMAND director.", "Say \"demand-plan director\" (or \"the demand director\")."),
 mk("N4", "note", "sweep-residue", "Drop-\"ladder\" coinage survives in live comments the sweep renamed around", "core/catalog.odin:184; core/crisis.odin:26,71,126,235,391; core/flow.odin:62,709(context); core/types.odin (Drop_Reason.Queue_Overflow comment); demos/qos_contention.dem, sla.dem, surge.dem comments; core/qos_test.odin + core/crisis_test.odin comments",
    "catalog.odin:184 `pool_max_packets: i32, // E22: in-flight cap; the spawn-side ladder drops at this depth` · crisis.odin:26 `a surge-class Queue_Overflow drop occurred this tick (the ladder just shed).`",
    "The ruled drop ladder → drop precedence rename covered many lines but left a constellation of live \"ladder\" mentions (some in files/lines the PR edited, some untouched). Comment-only; no behavior.", "Sweep the remaining drop-order \"ladder\" comments to \"drop precedence\" (leave the unrelated auto-reserve/cost/port ladders alone)."),
 mk("N5", "note", "over-rename", "Ordinary-English \"pressure\" mechanically renamed to \"congestion\" in canon docs, corrupting idioms", "gdd.md:73,107,291,367,430,478,555; epics.md:75,154; stories-v2.md:873",
    "gdd.md:107 `the player prioritizes and reroutes under time congestion` · epics.md:75 `**Delivers** modernization congestion.` · gdd.md:555 `congestion-riser stings`",
    "The verdict renamed the pipe-warning COINAGE (and kept the §M4 plumbing gloss); \"time pressure\"/\"modernization pressure\"/\"pressure-riser\" were everyday English, not coinage.", "Restore the idiomatic \"pressure\" (or reword) at those sites."),
 mk("N6", "note", "half-sweep", "stories-v2 half-sweeps: line-level mixes of old and new coinage", "stories-v2.md:365,295",
    ":365 `- **Goal.** Strain metrics from Topology + Flow → warning signs (🟡/🔴 node, pipe congestion, …` (the hunk renamed only \"pipe pressure\") · :295 `drops occur by the full ladder BE → Standard → Express [E9]`",
    "Canon sprint doc lines the PR edited carry the old coinage one clause away from the new.", "Finish the sweep on those two lines."),
 mk("N7", "note", "formatting", "ASCII diagram borders misaligned by un-padded renames", "gdd.md:84-89 (core-loop box, one row now 79 chars vs the 73/75 grid); odin-architecture-v1.md §5 component diagram",
    "old: `│  1. ASSESS  — read the live topology: node strain gauges, │` (75) → new: `│  1. ASSESS  — read the live topology: node congestion gauges, │` (79)",
    "Purely cosmetic, but the boxes no longer close in a straight column.", "Re-pad the affected rows."),
 mk("N8", "note", "grammar", "Mechanical-rename grammar warts", "core/types.odin:173 (`Amber = congested/congested`); core/warnings.odin:191 + node_health.odin (`never congestion` as a verb); core/node_health_test.odin (`must actually congestion a node`); spec-4-1 code map (`warning_evaluate (congestion, congestion, …)`); gdd.md M5 lead-times row (`congestion 20 s` among adjectives)",
    "types.odin:173 `// None = healthy (no telegraph); Amber = congested/congested; Red = critical.` (was `strained/pressured` — the two old words collapsed into one)",
    "Readable-but-broken prose left by the token substitution.", "Hand-fix each site (e.g. `Amber = congested`)."),
 mk("N9", "note", "sweep-residue", "Swept canon docs keep scattered old coinage/symbols", "odin-architecture-v1.md:731 + :1403 (`Set_Emphasis` intent); epics.md:48 (`priority-emphasis dial`); spec-4-1:26 (`Strain measure` heading); spec-traffic-model.md:149-150 (`scripted_plan_pressure`/`Pressure_Plan`); gdd.md:108 (`a straining bundle`); odin-architecture-v1.md:1042-1044 (`lane scheduling inside a link` / `the same 3 lanes` — two-tier: docs say class queue)",
    "arch:731 `` `Commit_Draw{node}`, `Select{target}`, `Cycle_Tier`, `Set_Emphasis`, `` — a live canon intent list naming a command kind that no longer exists",
    "Canon docs the PR swept still carry old coinage in spots (the historical per-story specs' authoring-time narrative is exempt — these are living canon surfaces).", "Sweep the listed sites."),
 mk("N10", "note", "naming-consistency", "\"emphasis\" vocabulary residue in live code: validate_set_emphasis/apply_set_emphasis proc names (the command is now Cmd_Set_Weights), qos_test/app \"emphasis\" comments, balance.json's \"3.2 emphasis-dial\" gloss, warnings.odin `press` local",
    "core/topology.odin:395,417; core/qos_test.odin (comments/assert msgs); app/main.odin comments; data/balance.json _comment; core/warnings.odin:174,187,228",
    "`validate_set_emphasis :: proc(t: ^Topology, c: Cmd_Set_Weights, cat: ^Catalogs) -> Edit_Error` · balance.json `_comment`: `lane_presets = the 3.2 emphasis-dial positions` · warnings.odin:174 `press := make([dynamic]i64, …)`",
    "The audit's ruled scope for the command rename was \"one union variant + comments\", so the procs were never ruled renamed — but the mismatch (procs named for a command that no longer exists) is now durable. Cosmetic; zero risk.",
    "Optional consistency sweep: validate_set_weights/apply_set_weights, the comment/gloss sites, `press` → `cong`.", ),
]

gate = {"sources": ["tests"], "severity": "note", "category": "coverage-gate",
 "title": "Advisory test gate: PASS",
 "location": "core/*_test.odin",
 "evidence": "odin test core: 183/183 green at b9d5006; Perkins' token-normalized hunk comparison proves EVERY test-delta line is rename-only (zero assertion/value changes).",
 "detail": "Every renamed symbol's tests renamed identically; expected event streams + reject matrices + replay pins unchanged. The c1 tests lens filed CONCERNS citing sweep residues; Perkins re-gated after mechanically proving zero assertion changes — the residues ride as their own notes (N1-N10).",
 "recommended_fix": "n/a", "verification": "confirmed", "lens_filings": len(members["GATE"])}
notes.append(gate)

rejected = []
for cid in ("REJECT-historical", "REJECT-out-of-scope", "REJECT-backcompat", "REJECT-misread"):
    for lens, chunk, x in members[cid]:
        rejected.append({"lens": lens, "chunk": chunk, "title": x.get("title"), "why": cid})

out = {
 "job": "packet-plumber-terminology-audit", "round": 1, "pr": 55,
 "reviewed_sha": "b9d500681acde12269b98566d42977c41e892adc",
 "reviewers_completed": 7, "failed_layers": [],
 "chunking": "16 file-group chunks (code 2,146 lines; docs 1,513; 14 golden chunks incl. fragments of growth/pause/health_win/surge) — canonical diff 39,829 lines / 110 files",
 "provider_incident": "deepseek 402 Insufficient Balance mid-round: waves g13/g14 + retries architecture-g11/codebase-g12 lost to it; redispatched on zai-coding-cn/glm-5.3 per the provider-incident doctrine (probe first, then sweep). All 112 lens outputs recovered; failed_layers empty.",
 "verification": {
   "raw_findings": 274,
   "merged_into_survivors": sum(len(members[c]) for c in ["W1","W2","N1","N2","N3","N4","N5","N6","N7","N8","N9","N10","GATE"]),
   "rejected_false_positive": sum(len(members[c]) for c in ("REJECT-historical","REJECT-out-of-scope","REJECT-backcompat","REJECT-misread")),
   "clusters": {c: len(members[c]) for c in ["W1","W2","N1","N2","N3","N4","N5","N6","N7","N8","N9","N10","GATE"]},
 },
 "blockers": [], "warnings": warnings, "notes": notes,
 "verdict": "READY TO MERGE", "review_event": "--approve",
 "perkins_verification": {
   "splice_proof": "REPRODUCED independently — scratch copy with ONE hook line (cat.hash forced to OLD bdc90b1363c93d8b; sim bytes untouched, diff -r clean): all 29 demos reproduce the OLD blessed goldens EXACTLY (every tick, ~22k ticks) and the OLD .log.bin files replay green. The fold is provably the only change.",
   "log_bin": "all 29 .log.bin diffs = exactly 8 bytes at offset 17 (the catalog_hash header field), old bdc90b1363c93d8b -> new 8f94df8eb817dddb, sizes identical",
   "t1_diff_shape": "every changed golden line is the catalog_hash header or a '<tick> <16hex>' line; tick numbering continuous 1..N with old==new counts on all 29; one uniform old->new catalog_hash pair",
   "t2_pixels": "ZERO .png entries in the diff; harness capture path never calls the app HUD (draw_hud absent from harness/) — the renamed legend string moves no golden pixel; harness run green = T2 byte-identical at this sha",
   "wire": "LOG_VERSION stays 4 (comment-only change); CMD_TAG value 5 kept (name-only); no payload layout touched",
   "rename_only": "token-normalized hunk comparison over ALL code/data/test files: every changed line is an identifier/comment/string rename — zero behavior deltas",
   "gates": "odin test core 183/183 green · tools/lint.sh 6/6 · harness run 29/29 (T1+T2+replay) · drift-check 204/204 mutations rejected",
   "residue_sweep": "Perkins' own old-identifier grep: zero old identifiers in live code paths; residues confined to comments/demo comments/catalog _comment/historical docs (the N-findings)",
 },
 "rejected_index": rejected,
}
json.dump(out, open(f"{R}/consolidated.json","w"), indent=1)
print("consolidated.json written")
print(json.dumps(out["verification"]["clusters"], indent=1))
print("raw:", out["verification"]["raw_findings"], "merged:", out["verification"]["merged_into_survivors"], "rejected:", out["verification"]["rejected_false_positive"])
EOF_MARKER_NOT_NEEDED = True
