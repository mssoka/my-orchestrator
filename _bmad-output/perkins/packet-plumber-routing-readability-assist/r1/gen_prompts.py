#!/usr/bin/env python3
"""Generate the 7 Perkins lens prompts for packet-plumber-routing-readability-assist r1 (single wave, no chunking)."""
import os

OUT = "/Users/moses/code/_bmad-output/perkins/packet-plumber-routing-readability-assist/r1"
WT = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-routing-readability-assist-r1"
SHA = "b0a6def"

DIFF = open(f"{OUT}/diff.patch").read()

SPEC_BLOCK = f"""  - Perkins briefing (your charter + the CRITICAL lens-guards): {OUT}/spec/perkins-briefing-r1.md
  - Job briefing (the original Job-A brief — context for what B builds on): {OUT}/spec/job-briefing.md
  - The canon (user ruling 2026-08-13 — PROBLEM DEFINITION, SUCCESS CRITERIA, RECOMMENDED SOLUTION with the R2a/R3/T2 package; this drives Job B): {OUT}/spec/canon.md
  - PR body (the minion's own launchable description): {OUT}/spec/pr-body.md
  - The minion's frozen spec is IN the diff itself (_bmad-output/implementation-artifacts/spec-routing-readability-assist.md) — the acceptance matrix + code map + the documented balance.json deviation."""

SCOPE = """Job B (readability package, app layer) on PR #40, targets `v2`. R2a live cost-sum flow preview while drawing (the draw ghost shows the path packets WILL take per the cost-aware routing table + the best path's total cost — ONE number or the delta, never a spreadsheet) + assist graduation tiers (full assist sum+glow DEFAULT -> partial glow-only -> off; settings toggle T; graduation nudge after N successful draws, N data-driven via data/assist.json, opt-in never forced); R3 post-draw route glow (the winning path lights up for glow_ticks); T2 equal-cost tie cue (BOTH tied paths marked "equal cost - split by hash"). STRICT view-only (ODN-12): reads the routing table + tier costs, NEVER feeds sim state, NO core changes. New files: app/render/assist.odin + data/assist.json + harness/assist_check.odin; additive palette keys; app/main.odin wiring. The harness `preview-check` verb (7 scenarios) cross-checks the preview against the sim's own routing."""

GUARDS = """- 🚨 LOAD-BEARING — STRICT VIEW-ONLY (ODN-12). The assist reads the routing table + tier costs and NEVER feeds sim state; NO core changes in this PR (verify: core/ untouched in the diff; a core modification = a blocker). The preview must show what the routing table WILL do — the preview path is CROSS-CHECKED against actual sim routing (the minion claims a preview-check harness, 7/7 — verify it exists and compares real vs previewed). The what-if table lives on an app-owned scratch CLONE; calling the public pure pp.routing_rebuild + pp.routing_equal_cost_hops from the app is ALLOWED (read contract), never modifying them.
- 🚨 LOCKED — do NOT flag as defects: Job A's Dijkstra model + the splice-proof re-bless (settled); `ecmp_pick`/`ecmp_hash` (pure identity hash — the tie-break is LOCKED, the visual cue rides beside it); the derived-not-serialized table; static costs; Job C's forecast panel (C owns app/render/forecast.odin — do NOT demand it here); per-class routing preferences (full-game, out of scope); no win/lose (4.3's job).
- THE FOUR ACCEPTANCE SURFACES: (1) R2a live preview: ONE number or the delta (never a candidate spreadsheet) + the draw ghost shows the cost-aware path; (2) assist graduation tiers: full/glow-only/off toggle (T) + the data-driven nudge (opt-in, NEVER forced — no modal); (3) R3 post-draw glow: the winning path lights up after a commit; (4) T2 tie cue: BOTH tied paths marked on ECMP (a split never looks random). Each surface must actually function (a toggle that doesn't toggle or a glow that never renders = a real defect).
- GOLDEN-DISCIPLINE: goldens byte-identical claim (the minion: harness 16/16 + goldens byte-identical) — verify; ANY golden shift = a finding (the assist is cosmetic and must not touch the capture path).
- ODN-5: data/assist.json additive + validated (a malformed config must fall back, not break the app). NOTE: the briefing said "N in balance.json"; the minion deliberately put N in the NEW cosmetic-class data/assist.json instead (balance.json folds into catalog_hash -> a field addition would re-bless ALL goldens, violating the golden-stability rule) — the spec documents this deviation and flags it for the human. Do NOT block on the deviation itself; DO flag any validation gap (malformed JSON bricking the app).
- Scope guard: Job B ONLY (app layer) — NOT C's forecast panel, NOT 4.3, NO new player commands (LOG_VERSION stays 3 — verify). app/main.odin is shared-risk with C (C is a SEPARATE open PR; review THIS diff at the sha).
- BASE = v2 (Job A + 4.2 merged — 69fc2e5). Em-dashes are OK in PP. ASCII-only string literals in render/app (lint gate 6 — the tie caption uses a hyphen, never an em-dash)."""

LEGIT = """- A view-only violation: assist/render code that mutates Run_State/Flow/Topology in place (the scratch clone is the only legal mutation target), a core/ change in the diff, or an app code path that changes sim behavior (e.g. a preview that allocates into live state, a glow read that races the step).
- Preview divergence from sim routing: the preview DAG/cost computed differently from what routing_rebuild + the flow's real forward pass would do (wrong first-affected-packet semantics vs flow.packets order, wrong on-edge starting node vs the E29 re-decision, wrong edge cost vs the table's min-bundle pricing, a candidate-edge membership test that ignores direction, stale partial DAG edges leaking between candidate packets).
- A broken surface: the R3 glow never rendering after commit (gen/tick gate mismatch — glow_gen captured pre-apply, the gate `tick <= glow_until && gen == glow_gen` can never be true), the T toggle not cycling or not dismissing the nudge, the nudge firing repeatedly/modal/forced, a tie cue that never draws on a real ECMP split or draws on a false split (a parallel-pipe bundle is NOT a split — the table dedupes per neighbor node), the route number showing alongside the cost readout (never two numbers).
- A golden shift: any goldens/*.t1 or *.log.bin or PNG differing from baseline 69fc2e5, or the harness capture path invoking the new draw procs.
- A config-validation gap: assist.json with negative/zero graduation_n, malformed JSON, or a wrong default_mode string bricking the app instead of falling back to inline defaults.
- A determinism/perf concern in the hot path: per-frame topology clone + full routing_rebuild every frame during a drag on a large map (assess the scale), a non-deterministic walk (map iteration), an allocation leak (preview buffers never released across runs).
- An acceptance-matrix miss: e.g. "no packet affected -> no glow, no number" not honored, the dead-end negative not covered, LOG_VERSION bumped or a new command added."""

CONTRACT = """Write ONLY a valid JSON array to your output file: {outfile}
No prose, no markdown fencing, no preamble, no trailing commentary. `[]` is valid and expected when you find nothing — do NOT invent findings to fill a quota.
Each element MUST match this schema exactly:
{
  "source": "{source}",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. view-only, preview-divergence, glow-lifecycle, tie-cue, golden-shift, config-validation, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the EXACT lines you READ from the file/diff that prove the claim, pasted verbatim. 'N/A' ONLY for findings with no possible code reference. Do not paraphrase; do not reconstruct from memory. If you cannot quote the lines, you have not done the work — drop the finding.>",
  "detail": "<why this is a problem, <=40 words; for acceptance findings quote the violated spec phrase>",
  "recommended_fix": "<the change to apply, <=40 words>"
}"""

ACCURACY = """ACCURACY MANDATE — the most important instruction: NO claim you make will be taken at face value. Every finding will be independently re-verified against the actual worktree before it reaches the report. Findings whose `evidence` cannot be located verbatim, or whose claim contradicts the code, are DISCARDED SILENTLY — no defense, no second chance. Therefore: OPEN the file, READ the cited lines. Quote them verbatim in `evidence`. Hedging ("might", "could", "possibly") signals you have NOT verified — either verify and report crisply, or drop it. Prefer fewer well-grounded findings over many speculative ones. An empty array is an honest, fine answer."""

BRIEFS = {
"blind": """You are a cynical, jaded reviewer with zero patience for sloppy work. BLINDNESS CONTRACT: the diff file is ALL the context you may use. Do NOT read the worktree, the specs, or any other file — reading anything beyond the diff INVALIDATES your lens. Assume problems exist; be skeptical; look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (the comments / commit message)""",

"edge": """You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, zero packets, no route, zero counts, max sizes), the live-drag vs committed-glow buffer interaction (cancel mid-drag, commit then re-drag, restart mid-glow), unhandled error paths in new code (JSON parse failures, node ids recycled across runs, a packet delivered mid-drag), off-by-one errors (tick/gate boundaries, glow expiry), state the new code doesn't account for (terminal run, no packets spawned yet, a dropped packet in the flow array), input the new code doesn't validate (config values).

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.""",

"acceptance": """Audit the diff against the spec and context docs above (the Perkins briefing's FOUR ACCEPTANCE SURFACES, the job briefing, the canon's R2a/R3/T2 + fun-factor + M6-M9, and the minion's own spec acceptance matrix inside the diff). Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible). The documented balance.json->assist.json deviation is PRE-ACCEPTED (spec-flags it for the human; the golden-stability rule wins) — do not file it as a violation; DO file any gap in its validation/fallback.""" ,

"security": """OWASP-oriented security review of the diff. This is a single-player desktop game (Odin + raylib) with JSON catalogs + a binary replay log + a demo parser — most OWASP categories will not apply; the realistic surface here is:
- Unsafe deserialization / missing validation at the NEW JSON boundary (data/assist.json parse in assist_config_load — type assertions like `v.(json.Object)`, `obj["graduation_n"].(json.Integer)`: can a malformed/malicious file panic or corrupt state?)
- Integer overflow/coercion at parse (i32 casts of unbounded JSON integers, u64 tick math)
- Input validation at system boundaries (the nudge/glow tick math, the candidate command built from UI coordinates)
- Any data exposure or credential concern (none expected)
`[]` is an honest answer. `source` = "security".""",

"architecture": """Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions (palette.json + fallback_palette pattern for the config, the render-layer separation, ODN-1 core purity, ODN-5 data-driven catalogs, ODN-12 view-only, ODN-13 no globals, ODN-10 arrays-only/no map iteration)?
- Does it introduce unnecessary coupling between modules (render -> core is by design here; is anything worse)?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns (the two-buffer ownership split, the scratch clone)?
- Will it create technical debt or make future changes harder (Job C lands on app/main.odin in a parallel PR — will this wiring collide)?
- Does complexity match the problem? Any premature abstraction (the per-frame full-topology clone + full routing rebuild during drag — assess against the game's scale)?""",

"codebase": """Reality check against the actual codebase (the worktree at the reviewed sha — {wt}). Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match? (pp.topology_make/routing_make/topology_destroy/routing_destroy, pp.node_slot, pp.bundles_slot_for_pair + bundle_lo/hi/tier/count fields, pp.routing_rebuild/routing_equal_cost_hops signatures, pp.ecmp_pick(src, dst, class, pkt_id, n), pp.topology_apply_edit, pp.Command{1, cmd} kind semantics, pp.Cmd_Draw_Pipe field names {from_node, to, tier}, pp.flow_seed_demand, pp.pipe_tier_index/node_type_index, Packet fields {on_edge, heading, at_node, delivered, src, dst, class, id}, rnd.to_screen/from_screen/node_screen/draw_text_c/tier_pipe_width/draw_text, WIN_W/WIN_H, the json.parse pattern in app/render/palette.odin)
- Are naming conventions and style consistent (lowercase procs are the house style — cross-package lowercase calls are established, do NOT flag them)?
- Does the diff duplicate logic that already exists elsewhere (e.g. a DAG walk or min-bundle-cost that core already provides)? Point to the existing helper in `location`.
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?""",

"tests": """Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80-89% OR P2 gap
- note: P3 gap

The P0 critical paths here: the preview == sim cross-check (harness/assist_check.odin run_assist_check — 7 scenarios: S1 fixture route, S2 fat-path shift, S3 true different-tier tie with T2 split, S4 dead-end negative, S5 mid-flight packet skip, S6 first-packet skip, S7 parallel-pipe no-op — each comparing the preview DAG/cost/splits against the sim's rebuilt table AND the packet's actual ecmp_pick path), the view-only contract (no core changes, no golden shifts — the harness `run` 16/16 + byte-identical goldens claim), the R3 glow lifecycle (glow_gen gate, two-buffer copy — is there ANY automated pin? the app layer has no unit tests today — assess whether the cross-check suffices or the glow/nudge/toggle logic is untested), the config fallback (malformed assist.json -> inline defaults — tested?), the nudge once-only latch, the T-toggle cycling.

Blind-spot heuristics: new state transitions without boundary tests (glow expiry exactly at glow_until, nudge at exactly N draws), happy-path-only coverage where error handling is implied (candidate illegal on the clone -> no preview; JSON fallbacks), test level mix (unit/integration/E2E) — flag mismatches.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS -> note, CONCERNS -> warning, FAIL -> blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100%, P1 >=90%, overall >=80%
- CONCERNS: P0 100%, P1 80-89%, overall >=80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%""",
}

for lens, brief in BRIEFS.items():
    outfile = f"{OUT}/{lens}.json"
    parts = [f"# Perkins lens prompt — {lens} (round 1, single wave)"]
    parts.append(f"**You are the `{lens}` lens. Your assigned `source` tag is `{lens}`. Your output file is `{outfile}`.**")
    parts.append("You are ONE lens in a Perkins automated PR-review swarm (round 1 of 3). Perkins reviews; lenses find; nobody fixes. You run as a pi agent. Review, then write your JSON and STOP — do not fix anything, do not modify any file other than your output file.")
    if lens == "blind":
        parts.append(f"## Your inputs (READ ONLY THESE)\n- CANONICAL DIFF (review exactly these bytes — read the file; it is the ONLY context you may use): {OUT}/diff.patch\n\n--- DIFF ---\n{DIFF}\n--- END DIFF ---")
    else:
        parts.append(f"""## Your inputs (READ THESE)
- CANONICAL DIFF (review exactly these bytes): {OUT}/diff.patch (embedded below for convenience)
- WORKTREE (read-only verification at the reviewed sha {SHA}): {WT}
- SPEC / CONTEXT:{SPEC_BLOCK}""")
        parts.append(f"--- DIFF ---\n{DIFF}\n--- END DIFF ---")
    parts.append(f"## The PR (scope)\n{SCOPE}")
    parts.append(f"## ⚠️ CRITICAL lens-guards — READ BEFORE FILING ANYTHING (prevents false positives)\n{GUARDS}")
    parts.append(f"## Legitimate findings here WOULD be\n{LEGIT}")
    parts.append(f"## YOUR LENS\n{brief}")
    contract = CONTRACT.replace("{outfile}", outfile).replace("{source}", lens)
    parts.append(f"## OUTPUT CONTRACT (follow exactly)\n{contract}")
    parts.append(f"\n{ACCURACY}")
    with open(f"{OUT}/prompts/{lens}.md", "w") as f:
        f.write("\n\n".join(parts))
    print(f"wrote {OUT}/prompts/{lens}.md ({os.path.getsize(f'{OUT}/prompts/{lens}.md')} bytes)")
