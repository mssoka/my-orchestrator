#!/usr/bin/env python3
"""Merge per-lens chunk outputs into <lens>.json, then write consolidated.json."""
import json, glob, os

OUT = "/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.1-packet-types/r1"
LENSES = ["blind", "edge", "acceptance", "security", "architecture", "codebase", "tests"]

# 1. Per-lens merged files (raw findings as filed, both chunks)
total_raw = 0
for lens in LENSES:
    merged = []
    for chunk in ("c1", "c2"):
        p = f"{OUT}/{lens}-{chunk}.json"
        merged += json.load(open(p))
    total_raw += len(merged)
    with open(f"{OUT}/{lens}.json", "w") as f:
        json.dump(merged, f, indent=1)
print("raw findings:", total_raw)

# 2. Consolidated, post-verification findings (deduped; sources merged; Perkins-verified)
def f(sources, severity, category, title, location, evidence, detail, fix, verification):
    return {"sources": sources, "severity": severity, "category": category, "title": title,
            "location": location, "evidence": evidence, "detail": detail,
            "recommended_fix": fix, "verification": verification}

findings = [
    f(["tests"], "blocker", "coverage-gap",
      "P0 gap: zero error-path tests for the new ODN-5 fail-fast catalog loaders (advisory test gate: FAIL, P0 5/6)",
      "core/catalog.odin:272-390",
      "grep: no core/*_test.odin calls catalogs_load; no malformed-input test exists anywhere. The two dozen new fail-fast rules (bad JSON, unknown shape/class_id/role/selection, latency/loss/bandwidth/lane/era bounds, set-piece multiplier/duration, required email/streaming) are exercised only happy-path via harness data loads.",
      "ODN-5 fail-fast is a named Story-3.1 AC ('catalogs are integer-only for sim values + fail-fast validated at load') with zero negative coverage; the gap already hides one live silent-default (the color_rgba !ok/!okc typo below). Gate thresholds: P0 <100% => FAIL.",
      "Add table-driven negative tests feeding malformed packet_types.json/demand.json byte strings to catalogs_load — one per fail-fast rule — asserting the named Catalog_Error file/field.",
      "confirmed"),
    f(["acceptance", "architecture", "blind", "codebase", "edge", "security", "tests"], "warning", "catalog-validation",
      "color_rgba element type guard is dead code (tests outer `ok`, not `okc`) — malformed element silently becomes 0 instead of fail-fast",
      "core/catalog.odin:295",
      "\t\t\t\t\tn, okc := arr[c].(json.Integer)\n\t\t\t\t\tif !ok || n < 0 || n > 255 {\n\t\t\t\t\t\treturn {\"packet_types.json\", pt.id, \"color_rgba must be 4 ints in 0..255\"}\n\t\t\t\t\t}",
      "`!ok` tests the outer `obj, ok := v.(json.Object)` binding (always true here); `okc` is never read. A non-integer color_rgba element (string/float) fails the cast, yields n=0, passes the range check — a silent default on malformed JSON, contra ODN-5. Field is cosmetic (secondary cue), hence warning not blocker.",
      "Change `if !ok ||` to `if !okc ||` so a non-integer color_rgba element hits the existing fail-fast return; add the negative test.",
      "confirmed"),
    f(["acceptance", "architecture", "blind", "edge", "security"], "warning", "catalog-validation",
      "Set-piece tick fields u64-wrap negative JSON values with no sign check — a negative start_tick silently never fires the surge",
      "core/catalog.odin:373-375",
      "\t\t\t\t\tsp.start_tick = u64(jint(seo, \"start_tick\", 0))\n\t\t\t\t\tsp.duration_ticks = u64(jint(seo, \"duration_ticks\", 0))\n\t\t\t\t\tsp.forecast_lead_ticks = u64(jint(seo, \"forecast_lead_ticks\", 0))\n\t\t\t\t\tif sp.multiplier < 1 || sp.duration_ticks == 0 {",
      "jint returns i32; u64(-5) wraps to ~2^64. start_tick -5 => set_piece_active false forever (silent demand loss); duration_ticks -1 passes the ==0 check and wraps (window arithmetic overflows). Out-of-range values accepted, contra the ODN-5 fail-fast bar.",
      "Read ticks into i32 locals and reject negatives (duration < 1) with a named Catalog_Error before the u64 casts.",
      "confirmed"),
    f(["architecture", "blind", "edge", "security"], "warning", "catalog-validation",
      "default_lane truncated to u8 BEFORE the >2 range check (both new loaders) — 256/257/258 wrap into valid lanes",
      "core/catalog.odin:306 and :356",
      "\t\t\tpt.default_lane = u8(jint(eo, \"default_lane\", 1))\n...\n\t\t\tif pt.default_lane > 2 {",
      "u8(jint(...)) wraps mod 256 before validation: JSON 256=>0, 257=>1, 258=>2 silently pass (CWE-681); only values wrapping to 3..255 are rejected. Same pattern in the demand-entry loader. ODN-5 fail-fast gap in the new 3.1 code.",
      "Range-check the i32 from jint before narrowing (`dl := jint(...); if dl < 0 || dl > 2 { return ... }`) at both sites.",
      "confirmed"),
    f(["codebase"], "warning", "catalog-validation",
      "Packet_Type.demand_weight has no range validation — negative weight loads silently (sibling fields are validated)",
      "core/catalog.odin:307-309",
      "\t\t\tpt.demand_weight = jint(eo, \"demand_weight\", 1)\n\t\t\tpt.era_introduced = jint(eo, \"era_introduced\", 1)\n\t\t\tif pt.latency_tol_ms <= 0 || pt.max_loss_pct < 0 || pt.max_loss_pct > 100 || pt.bandwidth_demand < 1 {",
      "The validation chain omits demand_weight, unlike Node_Type ('demand_weight must be >= 0', :235) and Demand_Entry (< 1 rejected, :358). A nonsense negative sibling weight reaches the 3.2/3.3 consumers unvalidated — ODN-5 consistency gap.",
      "Add a demand_weight bound (e.g. < 1) to the packet_types validation chain, matching the Node_Type/Demand_Entry precedent.",
      "confirmed"),
    f(["tests"], "warning", "coverage-gap",
      "weighted_pick_excluding untested: dst weighting pinned only for all-equal weights; all-excluded skip path never exercised",
      "core/flow.odin:125; core/demand_test.odin",
      "grep: weighted_pick_excluding has no direct test. The §3.3 flow-level pin (test_director_spawns_by_spec) uses demand_weight=1 on every sink, so a weights-ignoring dst pick would still pass it; only the weighted_pick primitive gets a non-uniform [1,2,3] distribution pin.",
      "The exclusion variant is the §3.3 rule's actual dst path: its per-sink demand_weight weighting, and its all-excluded => ok=false skip (a lone-sink topology silently spawns nothing), are uncovered. P1 gap.",
      "Unit-test weighted_pick_excluding: non-uniform-weight distribution pin, excluded slot never picked, all-excluded returns ok=false; add a single-sink flow_step test asserting the deterministic skip.",
      "confirmed"),
    f(["tests"], "warning", "coverage-gap",
      "Drift-check mutation matrix has no era-byte tamper class (the era byte became load-bearing in 3.1)",
      "harness/drift.odin:100-125",
      "make_drift_mutations covers catalog_hash/logic_hz/bad_magic/bad_version/bad_tag/truncation — six classes, no era flip (byte 16). drift_check asserts only replay_hashes acceptance, never the manifest compare.",
      "replay_hashes accepts era-tampered logs (era is APPLIED, not a rejection class) — the tamper is caught downstream by hash divergence at the compare stage (verified: run_demo's verify_replay gate is green end-to-end at 37f5581). The gap is drift-matrix completeness, not a silent acceptance.",
      "Add an era_flip mutation (byte 16) and have drift_check additionally assert the replayed hashes diverge from the manifest for applied-not-rejected classes.",
      "confirmed"),
    f(["architecture", "blind", "edge"], "note", "catalog-validation",
      "Duplicate demand era rows silently last-wins and leak the shadowed era's arrays",
      "core/catalog.odin:384",
      "\t\t\tfor len(cat.demand.eras) < int(era) { append(&cat.demand.eras, Demand_Era{}) }\n\t\t\tcat.demand.eras[era-1] = de",
      "No duplicate-era check: a second row with the same `era` overwrites the first; its demand content is silently dropped and its entries/set_pieces dynamic arrays leak (catalogs_destroy frees only stored rows). Duplicate content key should fail fast per ODN-5.",
      "Reject a row whose era slot is already populated (or track seen eras) with a named duplicate-era error before the assignment.",
      "confirmed"),
    f(["acceptance", "codebase"], "note", "doc-comment",
      "weighted_pick doc comment contradicts the code on zero/negative weights",
      "core/flow.odin:103-104",
      "// Array-order walk (no map-iter — ODN-10). A zero/negative weight is never\n// picked but still counts toward the total; total <= 0 -> ok=false.\n...\n\tfor w in weights {\n\t\tif w > 0 { total += u64(w) }",
      "The comment claims a zero/negative weight 'still counts toward the total'; the code excludes non-positive weights from `total` (demand_test.odin states the correct behavior). Code is correct; the comment misdescribes the load-bearing [E10] pick math.",
      "Reword to 'a zero/negative weight is never picked and is excluded from the total'.",
      "confirmed"),
    f(["blind"], "note", "leak",
      "load_demo_qos_fixture frees draws/spawns/captures but not demolishes",
      "harness/run.odin:253-258",
      "\tdemo, _ := parse_demo(demo_name, string(text_bytes))\n\tqos := demo.qos_fixture\n\tdelete(demo.draws)\n\tdelete(demo.spawns)\n\tdelete(demo.captures)\n\treturn qos",
      "Demo also owns demolishes ([dynamic]Demolish_Intent). Every call for a demo with demolish intents (drift_check and run_replay paths) leaks that array. Mirrors the same pre-existing omission in load_demo_spawns/load_demo_session, but the leak enters with this new function.",
      "Add `delete(demo.demolishes)` alongside the other frees (and optionally to the two sibling loaders).",
      "confirmed"),
    f(["codebase"], "note", "odn-5-integer-only",
      "jint silently truncates json.Float — non-integer values accepted on the new 3.1 sim fields",
      "core/catalog.odin:507-513",
      "jint :: proc(o: json.Object, key: string, def: i32) -> i32 {\n\tif v, ok := o[key]; ok {\n\t\t#partial switch x in v {\n\t\tcase json.Integer: return i32(x)\n\t\tcase json.Float:   return i32(x)",
      "The new 3.1 loaders read sim values via jint (e.g. de2.volume = jint(eeo, \"volume\", 0)): `\"volume\": 2.9` loads as 2 with no error. The helper is carry-forward from 1.2, but its float truncation now silently admits non-integer values into the new catalogs, weakening the integer-only ODN-5/ODN-10 bar.",
      "For the new 3.1 sim fields, reject json.Float (fail fast) instead of truncating — a strict jint variant that errors when the value is not json.Integer.",
      "confirmed"),
    f(["codebase"], "note", "harness-allocator",
      "T2 failure messages are temp-allocated inside the tick loop and freed by the per-tick free_all before the post-loop FAIL print",
      "harness/run.odin:128-132 + :165-167; harness/goldens.odin:109",
      "\t\t\t\t\t\tcheck_golden(name, cap_ms, img, &report, &fails)   // appends fmt.tprintf (temp) messages\n...\n\t\tfree_all(context.temp_allocator)   // end of every tick\n...\n\tfor m in fails {\n\t\tfmt.printf(\"    - %s\\n\", m)   // reads the freed strings",
      "check_golden's fmt.tprintf mismatch messages are temp-allocated; free_all at each tick end frees them; the FAIL print loop after the run emits freed memory (NULs/garbage) — the failure detail (mismatch count, diff-bundle path) is unreadable exactly when T2 fails. PASS/FAIL gating itself is unaffected (len(fails) is sound).",
      "Allocate the fails strings (or check_golden's messages) with context.allocator, or defer the per-tick free_all of those strings until after the report is written.",
      "confirmed"),
    f(["acceptance"], "note", "demo-spec-consistency",
      "qos.dem is the only demo missing the `expect hash stable` declaration (directive is parsed but never read)",
      "demos/qos.dem",
      "demos/qos.dem tail: `capture at 1000ms / capture at 65000ms` — no `expect hash stable` (all 7 other demos carry it). grep: expect_hash_stable is written at harness/demo.odin:121 and never read anywhere.",
      "Convention drift: the new era-3 golden breaks the 8-demo pattern. Zero behavioral effect today (the replay gate runs unconditionally; the field is dead) — flagged so the convention stays uniform or the dead directive gets removed deliberately.",
      "Add `expect hash stable` to demos/qos.dem to match the other 7 demos (or remove the dead directive from all demos + the parser).",
      "confirmed"),
]

rejected = [
    {"source": ["blind"], "severity_filed": "blocker", "title": "Era applied from header.era on replay but no hunk writes era into the log header",
     "reason": "False — the log-header era plumbing pre-exists this diff (core/serialize.odin:78 `w_u8(&w, state.era)` writes it, :266 `h.era = r_u8(&r)` parses it; neither hunk is touched by the PR). Empirically falsified: the era-3 qos golden replays bit-for-bit (harness 8/8 green at 37f5581) — impossible if replay applied era 0 (the director would spawn nothing and the 1500-tick re-sim would diverge at tick 1)."},
    {"source": ["blind"], "severity_filed": "note", "title": "Non-object rows in packet_types/demand arrays silently skipped via or_continue",
     "reason": "Pre-existing house pattern in every loader since 1.2 (node_types :219, pipe_tiers :255 — merged, Perkins-verified); the new loaders mirror it consistently. Carry-forward guard: not a finding against this PR."},
    {"source": ["blind"], "severity_filed": "warning", "title": "bundle/lose PNGs re-captured despite expectation only flow/+qos/ change",
     "reason": "Fully explained by the class-0 render change: exactly the demos with a VISIBLE in-flight packet at a capture re-blessed PNGs (flow x3; bundle@2850ms is post-spawn 'carrying traffic'; lose@3000ms pins the stuck packet). draw/boot/win/demolish have no visible packet at capture and did NOT re-capture. T2 pixel-diff deferral (rlsw gap) covers pixel-level verification."},
    {"source": ["blind"], "severity_filed": "note", "title": "draw/flow/win share byte-identical .log.bin while .t1 manifests diverge",
     "reason": "By design: identical seed (42) + identical draw commands; spawns/session/era are run setup, NOT logged (re-created from the .dem on replay — load_demo_spawns/session/qos_fixture). Empirically green: all three replay bit-for-bit to their divergent manifests at 37f5581."},
]

counts = {"blocker": 0, "warning": 0, "note": 0}
for x in findings:
    counts[x["severity"]] += 1

consolidated = {
    "job": "packet-plumber-v2-3.1-packet-types",
    "round": 1,
    "pr": 28,
    "reviewed_sha": "37f5581756345d1e41d16901b303808b3c9ccede",
    "diff_file": f"{OUT}/diff.patch",
    "chunking": "diff 4013 lines > ~3000 => two file-group chunks, one full 7-lens wave each, sequentially: chunk1 = app+core+data+demos+harness (1387 lines, 16 files), chunk2 = goldens (2626 lines, 23 files). Findings merged before verification.",
    "worktree": "/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-3.1-packet-types-r1",
    "reviewers_completed": 14,
    "reviewers_total": 14,
    "failed_layers": [],
    "total_findings": total_raw,
    "unique_after_dedupe": len(findings) + len(rejected),
    "verified_confirmed": len(findings),
    "rejected": len(rejected),
    "unverifiable_speculative": 0,
    "counts": counts,
    "verdict": "NEEDS CHANGES",
    "verdict_reason": "1 blocker: zero error-path tests for the new ODN-5 fail-fast catalog loaders (a named Story-3.1 AC) — the gap already hides one live silent-default (color_rgba !ok/!okc, 7-lens agreement). All load-bearing invariants verified GREEN at 37f5581: distinct shapes (circle/triangle, never color alone), spawn determinism [E10] (one seeded draw per pick inside the stream; era-0 draws zero rng), director read-only [ODN-7], core engine-free [ODN-1], §3.3 dst-distribution pin real, era-3 QoS golden replays bit-for-bit; odin test 59/59, harness 8/8, lint 5/5.",
    "findings": findings,
    "rejected_findings": rejected,
}
with open(f"{OUT}/consolidated.json", "w") as fh:
    json.dump(consolidated, fh, indent=1)
print("consolidated.json written:", counts, "verdict:", consolidated["verdict"])
