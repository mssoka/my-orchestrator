#!/usr/bin/env python3
"""Consolidate the 35 lens outputs into consolidated.json for packet-plumber-v2-4.1-warning-forecast r1."""
import json, glob, os

OUT = "/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.1-warning-forecast/r1"

raw = []
for f in sorted(glob.glob(f"{OUT}/*-c[1-5].json")):
    d = json.load(open(f))
    for x in d:
        x["_file"] = os.path.basename(f)
        raw.append(x)

# ---- verification results (Perkins's own mandatory verification pass) ----
# Every finding below was re-checked against the worktree at 9820a55.
# Dropped findings:
#   - blind-c1 "negative lead wraps" (merged into W3)
#   - blind-c5 "four captures byte-identical" — POSITIVE: the four blobs were
#     identical at base too (shared fixture scene); the re-bless moved them
#     together; sla/10000ms.png blob identical pre/post (relief-frame proof).
#   - tests-c1 "stuck+healthy mixture" (merged into N7)
#   - all golden-structure notes from c2/c3/c4 with no defect ([] waves)

findings = [
{
 "source": ["tests"],
 "severity": "blocker",
 "category": "coverage-gate",
 "title": "Advisory test gate: FAIL — the warning-event ladder is half-unpinned",
 "location": "core/warnings_test.odin; core/warnings.odin:89-105",
 "evidence": "core/warnings_test.odin test_node_strain_amber_red_clear pins only None→Amber (@2 RAISED Node_Strained), Amber→Red (@3 RAISED Node_Critical), Red→None (@8 CLEARED Node_Critical); the node Red→Amber easing (CLEARED Node_Critical while strained persists) and Amber→None (CLEARED Node_Strained) branches of node_strain_transition (core/warnings.odin:89-105) have no test; the pipe twin covers its full ladder. Multi-member-bundle pressure replication (warnings.odin:212-223) is exercised by no test or demo (all scenarios + warn.dem use single-member bundles).",
 "detail": "P0/P1 coverage below the gate: 2 of 5 node transitions + replication + router/residential pins + exact 70/90 boundaries untested; warn.dem exercises only Red→None. Gate FAIL per the tests brief.",
 "recommended_fix": "Add tests: node Red→Amber easing + Amber→None cleared-sign; a two-pipe parallel bundle pressure-replication pin; router 75%/150% + residential 600% ladder pins; exact 69/70/89/90/91 boundaries.",
 "verification": "confirmed",
},
{
 "source": ["acceptance", "architecture", "blind", "codebase", "edge"],
 "severity": "warning",
 "category": "accessibility",
 "title": "Health-ring pulse runs 16× slower than the documented escalation rates (0.078/0.156 Hz delivered vs 1.2/2.5 Hz pinned)",
 "location": "app/render/view.odin:204-213, 334-345",
 "evidence": "PULSE16 is 16 steps; pulse_factor idx = (tick + node_id*5) / step & 15; draw_health_ring passes step=16 (amber) and step=8 (red) → cycle = 16×16 = 256 ticks = 12.8 s (0.078 Hz) and 16×8 = 128 ticks = 6.4 s (0.156 Hz). The comment claims 'slow amber pulse ~1.25 Hz' (needs step=1) and 'fast critical pulse ~2.5 Hz' (impossible with a 16-step table; step=2 would be 0.625 Hz). epic-4-context.md: 'the ring pulse rate is itself the escalation signal: slow ~1.2 Hz strained, fast ~2.5 Hz critical'.",
 "detail": "The motion encoder of the triple-redundant telegraph is effectively static (12.8 s cycle) and contradicts the PR's own comments + design doc. Not color-only (ring+glyph hold), so not a blocker.",
 "recommended_fix": "Amber step=1 (1.25 Hz); red needs a faster envelope (e.g. idx & 7 → 8-step cycle = 2.5 Hz) or accept 1.25 Hz and fix both comments.",
 "verification": "confirmed",
},
{
 "source": ["architecture", "blind", "edge"],
 "severity": "warning",
 "category": "dead-config",
 "title": "balance.json warning lead times (600/200/400) are parsed + validated + folded into catalog_hash but never consumed — the claimed telegraph lead surface does not exist",
 "location": "core/catalog.odin:192-200, 532-534; app/render/view.odin; app/render/forecast.odin",
 "evidence": "grep across core/app/harness: node_strained_lead_ticks / node_critical_lead_ticks / pipe_pressure_lead_ticks appear only in Warning_Balance (types/catalog), the parse (catalog.odin:532-534) and the >0 check (541-542). catalog.odin:189-191 comment claims 'The UI reads the leads from here for the telegraph'; warnings.odin header claims 'the UI reads them from there' — neither is true. The forecast panel reads sp.forecast_lead_ticks (per-set-piece), not these.",
 "detail": "FORGE #3 lead-time surface: the amber stage (70→90 gap) is the only operational lead; the three balance keys are dead config that still shifts every golden via the fold.",
 "recommended_fix": "Either consume the leads in the telegraph (e.g. a countdown-to-critical caption) or strike the 'UI reads the leads' claims and document the amber stage as the lead.",
 "verification": "confirmed",
},
{
 "source": ["security", "edge", "blind", "architecture"],
 "severity": "warning",
 "category": "validation",
 "title": "Negative lead-time JSON values wrap through u64() and defeat the 'leads > 0' fail-fast",
 "location": "core/catalog.odin:532-534, 541-543",
 "evidence": "b.warnings.node_strained_lead_ticks = u64(jint(wobj, \"node_strained_lead_ticks\", 0)) — jint returns i32; u64(i32(-1)) wraps to 18446744073709551615, which passes the `== 0` rejection at 541-543.",
 "detail": "A content bug (negative lead) silently accepted despite the named fail-fast; catalog_hash pins the bad value into every golden.",
 "recommended_fix": "Check the i32 before casting: reject < 0 (or parse via jint_strict) before u64 conversion.",
 "verification": "confirmed",
},
{
 "source": ["security", "architecture"],
 "severity": "warning",
 "category": "validation",
 "title": "A partial warnings block (missing node_amber_pct/pipe_amber_pct) defaults to 0 and makes every healthy node permanently Amber",
 "location": "core/catalog.odin:528-539; core/warnings.odin:71-77",
 "evidence": "jint(wobj, \"node_amber_pct\", 0) defaults missing keys to 0; the ladder check (536-538) accepts 0 <= amber < red <= 100; strain_level returns .Amber for any pct >= 0, so every alive node with throughput > 0 reads Amber even at zero strain — breaking the absent-when-empty/zero-traffic contract.",
 "detail": "Legal-but-bad data silently breaks the no-warning-when-healthy invariant; the fail-fast exists to catch exactly this class.",
 "recommended_fix": "Reject amber == 0 (amber must be > 0), or require the full warnings block present.",
 "verification": "confirmed",
},
{
 "source": ["acceptance", "architecture", "blind", "codebase", "edge", "security", "tests"],
 "severity": "warning",
 "category": "goldens",
 "title": "qos/01000ms.png re-blessed (verified real: E9-bound red pipe-pressure halos from ~tick 8-20) but missing from the implementation spec's per-demo cause list, which names only qos's 65 s capture",
 "location": "goldens/qos/01000ms.png; _bmad-output/implementation-artifacts/spec-4-1-warning-forecast.md 'Golden' bullet",
 "evidence": "diff.patch c3: goldens/qos/01000ms.png 41451 -> 42082 bytes (Binary files differ). Spec line 33: 'qos.dem's 65 s capture (the panel + surge strain)' is the only qos T2 shift enumerated; the 1 s capture shift is unlisted. Lenses sim-verified the shift is honest (lanes at the E9 bound at tick 20 → real halos).",
 "detail": "The shift is honest and consistent with the documented mechanism ('a demo that strains at a capture gains rings/halos'), but the per-demo enumeration is incomplete — a future reviewer would flag it as unaccounted.",
 "recommended_fix": "Add the 1 s capture to the qos.dem cause-doc (and audit the other captures for the same omission).",
 "verification": "confirmed",
},
{
 "source": ["tests", "tests", "tests", "tests"],
 "severity": "warning",
 "category": "coverage",
 "title": "Router (1 stuck = 75 % amber, 2 = 150 % red) and residential (any stuck = 600 % red) strain-ladder pins have no direct test — only the content_host ladder is pinned",
 "location": "core/warnings_test.odin:70-106; spec-4-1-warning-forecast.md Design Notes",
 "evidence": "test_node_strain_amber_red_clear strains only the host (throughput 80): 2 waiting = 75 %, 3 = 112 %. The design notes' router/residential pins (40 u/s → 1 packet = 75 %, 2 = 150 %; 5 u/s → any = 600 %) are exercised by no unit test; warn.dem covers the residential via golden only.",
 "detail": "The story's own numerical pins for two of three node types are unpinned at the unit level.",
 "recommended_fix": "Add a router-ladder test (1/2 stuck packets on a router) and a residential 600 % pin.",
 "verification": "confirmed",
},
{
 "source": ["acceptance", "codebase"],
 "severity": "note",
 "category": "copy",
 "title": "Run-HUD still instructs 'deliver a packet to win' in the 4.1 sandbox where win/lose is disabled (goal 0 / cap 0)",
 "location": "app/main.odin:533",
 "evidence": "draw_text(app, \"draw source->router->sink; deliver a packet to win\", 12, 36, 16, p.ink_soft) — unconditional; WIN_GOAL :: u32(0) / LOSE_TICK_CAP :: u64(0) at main.odin:32-33. The promised win never fires (win/lose is 4.3's).",
 "detail": "Misleading instruction in the launchable sandbox; the score readout correctly hides the goal (goal > 0 branch), but the instruction line is stale.",
 "recommended_fix": "Reword for the sandbox (e.g. 'survive the surge; watch the telegraph') or gate on goal > 0.",
 "verification": "confirmed",
},
{
 "source": ["architecture"],
 "severity": "note",
 "category": "labeling",
 "title": "Forecast panel hardcodes 'SURGE' for every set-piece row instead of reading an archetype name",
 "location": "app/render/forecast.odin:52",
 "evidence": "mult := fmt.aprintf(\"SURGE x%d\", f.multiplier, ...) — the archetype label is a literal; the class display name comes from the catalog, but the archetype word never does. Any future non-surge set-piece (the era catalog supports arbitrary ids) renders as 'SURGE'.",
 "detail": "Cosmetic today (only the streaming surge exists), but mislabels future set-pieces; the catalog has no archetype field to read.",
 "recommended_fix": "Add an archetype display field to the set-piece catalog row and read it here.",
 "verification": "confirmed",
},
{
 "source": ["codebase"],
 "severity": "note",
 "category": "docs",
 "title": "Frozen spec self-contradiction: Design Notes + Verification list lose among 'must stay pixel-identical' T2 demos while its own Boundaries cause-doc shifts lose.dem",
 "location": "_bmad-output/implementation-artifacts/spec-4-1-warning-forecast.md:95,106 vs :33",
 "evidence": "Line 95: 'boot/draw/place/flow/win/lose/ecmp/bundle/demolish T2s must stay pixel-identical (the negative proof)'; line 106: 'tools/harness.sh save boot draw place flow win lose ecmp bundle demolish -- must be T2 no-ops'. Line 33 (Boundaries): 'lose.dem (its own stuck packet — the demo's scenario IS the strain: the residential telegraphs 🔴, cause-documented)' — and goldens/lose/03000ms.png IS in the diff.",
 "detail": "The code follows the Boundaries cause-doc correctly; the Design Notes/Verification lists are stale and would mislead a future reviewer into flagging lose's PNG.",
 "recommended_fix": "Remove lose from the pixel-identical lists at lines 95 and 106.",
 "verification": "confirmed",
},
{
 "source": ["tests"],
 "severity": "note",
 "category": "test-helper",
 "title": "qos_first_word_after_topology walker does not skip the SLA (3.4) or warnings (4.1) serialized sections — latent misparse on any strained dump",
 "location": "core/qos_test.odin:284-319",
 "evidence": "The walker reads header → flow packets (now 12 fields incl. waiting_ticks) → demand → next_packet_id → then 'topology nodes'. state_writer (serialize.odin) inserts the SLA section (3.4) and the warnings section (4.1) between next_packet_id and the topology. It passes today only because the calling tests' dumps have both sections absent-when-empty.",
 "detail": "Latent test-helper fragility: a future call on a dump with SLA/warnings bytes silently misparses counts. Not a live failure (97/97 green).",
 "recommended_fix": "Skip the SLA + warnings sections in the walker (mirror the writer's absent-when-empty rule).",
 "verification": "confirmed",
},
{
 "source": ["tests", "tests", "tests"],
 "severity": "note",
 "category": "coverage",
 "title": "Smaller warning-test gaps: exact 69/70/89/90/91 boundaries, dead-node-slot never-warns path, demolished-node resident packets, stuck+healthy mixture, E29 drop-back clear, forecast-purity assert, era-3 session pin",
 "location": "core/warnings_test.odin; core/demolish_test.odin; app/main.odin:32-34",
 "evidence": "All strain pins cross thresholds strictly (75/112/100/83/67/600 %) — inclusive lower bounds at exactly 70/90 unexercised; warning_evaluate dead-slot path (warnings.odin:200-202, sets .None with no CLEARED event) untested; demolished-node resident packets (flow.odin:753 E29 drop-back clears waiting_ticks) have no crisis-interaction test; the no-flicker test uses pure transits and the ladder test pure stuck — no mixture; test_forecast_window_rows clears events without asserting they stayed empty; app session constants (WIN_GOAL 0 / LOSE_TICK_CAP 0 / APP_ERA 3) have no automated pin.",
 "detail": "Each is small; together they define the next coverage increment for the 4.1 contract.",
 "recommended_fix": "Add: boundary-70/90 pin, dead-slot test (demolish mid-run → no events, no strain), mixture test, E29 clear assert, forecast purity assert, session-config pin.",
 "verification": "confirmed",
},
{
 "source": ["tests"],
 "severity": "note",
 "category": "coverage",
 "title": "Tag-conditional event byte-layout (pre-4.1 event bytes unchanged) has no dedicated regression pin — masked by the full re-bless",
 "location": "core/serialize.odin:352-354",
 "evidence": "The event payload writes are tag-conditional (w_u8 sign + w_u32 target only for tags 6/7); verified correct by reading, but no unit test walks the event bytes for an old tag asserting zero payload bytes. The .t1 goldens would catch a layout change only when the event stream is non-empty AND the golden isn't re-blessed over it.",
 "detail": "After a full re-bless, a subtle event-bytes regression could be baked into the new goldens silently; the replay test pins equality but not the byte layout.",
 "recommended_fix": "Add a state_dump byte-walk asserting old-tag events serialize exactly their pre-4.1 field set.",
 "verification": "confirmed",
},
{
 "source": ["blind"],
 "severity": "note",
 "category": "goldens",
 "title": "Four re-blessed strain captures (sla 1 s/4 s, qos_contention 1 s/10 s) are byte-identical to each other before and after the re-bless — a consistency property, not a defect",
 "location": "goldens/sla/01000ms.png; goldens/sla/04000ms.png; goldens/qos_contention/01000ms.png; goldens/qos_contention/10000ms.png",
 "evidence": "git blobs: base 3c26f469… shared by all four; head 04898696… shared by all four — the shared fixture scene shifts together. sla/10000ms.png blob aee15ead… is identical pre/post (relief frame untouched).",
 "detail": "Verified positive: the four captures share one scene and the re-bless moved them consistently; the relief-frame negative proof holds inside the shifted demo.",
 "recommended_fix": "None.",
 "verification": "confirmed-positive",
},
]

# order: blockers, warnings, notes
def key(x):
    return {"blocker": 0, "warning": 1, "note": 2}[x["severity"]]

findings.sort(key=key)

consolidated = {
    "job": "packet-plumber-v2-4.1-warning-forecast",
    "round": 1,
    "sha": "9820a55e0541d8d7b5e114f9a486726e4df83141",
    "pr": 35,
    "repo": "solarity-services/Packet-Plumber",
    "chunks": {
        "c1": "code+docs+data+demos+harness (21 files, 1676 lines)",
        "c2": "warn.dem goldens (5 files, 1529 lines)",
        "c3": "qos.dem golden (4 files, 3020 lines)",
        "c4": "light-demo goldens — negative proof (19 files, 1437 lines)",
        "c5": "contention/era-3 goldens sla+qos_contention+qos_emphasis (14 files, 1626 lines)",
    },
    "lens_waves": {f"c{i}": "7/7 complete" for i in range(1, 6)},
    "failed_layers": [],
    "raw_findings": len(raw),
    "findings": findings,
    "counts": {
        "blockers": sum(1 for f in findings if f["severity"] == "blocker"),
        "warnings": sum(1 for f in findings if f["severity"] == "warning"),
        "notes": sum(1 for f in findings if f["severity"] == "note"),
    },
    "verdict": "NEEDS CHANGES",
}

with open(f"{OUT}/consolidated.json", "w") as f:
    json.dump(consolidated, f, indent=2)
print(json.dumps(consolidated["counts"]), "->", consolidated["verdict"])
