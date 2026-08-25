#!/usr/bin/env python3
"""Generate the 7 Perkins lens prompts for packet-plumber-v2-harness-ecmp-demo r1."""
import os

OUT = "/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-harness-ecmp-demo/r1"
WT = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-harness-ecmp-demo-r1"
SHA = "f90351da"

SPEC_BLOCK = f"""  - Perkins briefing (your charter + lens-guards): {OUT}/spec/perkins-briefing-r1.md
  - Job briefing (the implementing minion's spec): {OUT}/spec/job-briefing.md
  - Architecture invariants: {OUT}/spec/odin-architecture-v1.md — §10 The golden-image harness (line 1326), §10.4 rlsw + PLATFORM_MEMORY bit-exact pixels (line 1407), §10.7 harness build & CI (line 1474), ODN-1 core-engine-free (line 410), ODN-10 integer math + array-only iteration (line 643), ODN-11 action-log replay (~line 399 + §11.4 line 1556), ODN-17 harness first-class (line 792), §11.7 edge-case table (line 1592; E10 at line 1609)
  - The README golden-harness section + the .dem format docs live in the worktree itself (README.md, demos/*.dem)"""

SCOPE = """PP v2 infra mini-story (deferred from 2.2's rec): the rlsw SW-renderer harness + node-spawn demo directive + ecmp.dem + T2 retro-verify for 2.1/2.2/2.3. Single wave, 663-line diff, 7 file groups:
- demos/demolish.dem — MODIFIED: adds 4 T2 pixel captures (1050/1250/1300/3000ms) + a comment rewrite (the demolish replay semantics unchanged; T1 hashes + replay gate still pin the rest)
- demos/ecmp.dem — NEW: a diamond topology built entirely via `fixture off` + 4 `spawn_node` lines (ids 0..3 = spawn order); 4 edges drawn at 500ms; 4 packets spawned residential(0)->content_host(3) at 1000-1300ms, ECMP hash splitmix64(src,dst,class,pkt_id) mod 2 spreads them m1/m2; captures at 1250/1350/3000ms
- goldens/demolish/*.png (4 NEW — first-bless), goldens/ecmp/*.png (3 NEW — first-bless), goldens/ecmp.t1 (NEW, 80 ticks @20Hz = 4000ms, seed 42), goldens/ecmp.log.bin (NEW)
- harness/demo.odin — Node_Spawn struct + `spawn_node <type> <x> <y>` and `fixture on|off` parse verbs; spawn_node type_name strings.clone'd (temp-arena lifetime note)
- harness/run.odin — Demo_Replay single-struct (fixture toggle + spawn_node topology + spawn demand + win/lose session) threaded through run_demo + replay_hashes; demo_apply_setup single-source; load_demo_replay replaces load_demo_spawns/load_demo_session; lower_nodes resolves type names against the catalog (fail-loud) and calls pp.topology_spawn_node in file order
- harness/drift.odin — drift_check ported to load_demo_replay/Demo_Replay
- harness/goldens.odin — allocator-discipline fixes (fmt.tprintf -> fmt.aprintf for strings that outlive the per-tick temp free_all) + a JSON format-string change (`{` -> `{{`) in the diff-bundle diff.json writer
The claim: harness/demo-only; core untouched; 8/8 demos T1+T2+replay green; drift 47/47; odin 54/54."""

GUARDS = """- **🚨 GOLDEN-BLESSING DISCIPLINE — THE load-bearing invariant.** A pixel MISMATCH against an ALREADY-blessed golden (bundle/flow/draw/win/lose) = a REAL blocker (drift). But the ecmp + demolish goldens are **FIRST-BLESS**: their pixel content was blessed in this very PR — do NOT flag "new golden files added" as a defect; instead VERIFY the blessing path actually ran pixel-verification (mismatch → finding, never a silent re-bless / blind accept). A first-bless done through the real comparison path is the contract; a skip/force-accept is a defect.
- **🚨 rlsw BIT-EXACTNESS [PLATFORM_MEMORY] — load-bearing.** The harness renders in the SW renderer (`PLATFORM_MEMORY`, no GPU) so goldens are platform-independent (`-ffp-contract=off`). Do NOT flag "goldens are platform-dependent" or "no GPU path" — that's the design. A golden generated through a NON-deterministic path (unbounded float ops, unseeded RNG in the render, map-iter order in the pixel path) = a blocker.
- **NODE-SPAWN DETERMINISM [E10].** `spawn_node` assigns ids in SPAWN ORDER (deterministic); the demo script drives a fixed sequence. An id assigned by anything order-independent-in-practice but not guaranteed (map iteration, hash order, pointer value) = a real defect — the same discipline as ECMP (array-indexed, no map-iter in the hot path).
- **HARNESS IS INFRA, NOT PRODUCTION.** The harness/demos live OUTSIDE the core engine and the app's production path (core engine-free [ODN-1] — zero core imports in the harness). Do NOT flag "harness code isn't in the game binary" or "demo content is trivial" — the harness is a dev/verification tool; its job is to prove the demos, not ship gameplay.
- **Demo_Replay SINGLE-STRUCT decision (routing-ruling lens-guard).** The replay is a single struct (`Demo_Replay`), NOT per-demo variants — a deliberate simplification the minion documented. Do NOT flag "replay should be per-demo polymorphic".
- **FIXTURE OPT-OUT (documented decision).** The demo fixture (T2 pixel fixtures) is opted out of the `odin test` runner deliberately — the pixel verification runs through the harness demos instead (8/8 demos T1+T2+replay). Do NOT flag "fixture tests missing from odin test" — the harness demos ARE the fixture verification.
- **CORE UNTOUCHED.** The 2.1/2.2/2.3 core stories are MERGED and Perkins-verified — do NOT re-open their findings; carry-forward only. If this PR touches core engine logic, THAT is worth flagging (it claims to be harness/demo-only).
- **Em-dashes are FINE in Packet-Plumber copy** (the RT CI ban does NOT apply to PP).
- **The base is `v2`**, not `main`. The prototype (if visible in the repo) is REFERENCE-ONLY.
- **Do NOT re-open 1.1–2.3 findings** (merged, Perkins-verified) — carry-forward only."""

LEGIT = """- **Golden DRIFT** — a previously-blessed golden (bundle/flow/draw/win/lose) whose pixels changed without a matching, documented, verified re-bless — a blocker.
- **A silent re-bless / forced-accept golden path** (skipped pixel verification, blind overwrite) for the NEW ecmp/demolish goldens — a blocker.
- **A non-deterministic render or spawn path** (unseeded RNG draw, map-iter in the pixel/spawn path, float-op order dependence) — a blocker [E10]/bit-exactness.
- **A `spawn_node` id assigned by hash/pointer/map order** instead of spawn order — a real defect.
- **Core engine logic changed by this PR** (it claims harness/demo-only) — a real defect [ODN-1].
- **An `odin test` / `odin build` / `harness` failure at f90351da** (the drift + demo gates are real: drift 47/47, demos 8/8).
- Also worth checking: ecmp.t1 header consistency (ticks 80 = 4000ms x 20Hz; seed 42; catalog_hash matches sibling goldens); the diff.json writer's `{` -> `{{` format-string change in harness/goldens.odin (does Odin's fmt treat `{{` as an escaped literal? verify against core:fmt behavior — if it prints literal `{{` the diff.json is invalid JSON on the mismatch path); spawn_node parse bounds (negative/huge coords, missing fields, unknown type fail-loud vs silent); the strings.clone/delete pairing on every exit path (parse error returns, load_demo_replay early returns); the Demo_Replay sharing discipline (run_demo's cfg SHARES type_name strings with the live Demo — is demo_replay_destroy correctly NOT called there?); fixture off + spawn_node interplay with demos that spawn packets referencing node ids."""

OUTPUT_CONTRACT = """Write ONLY a valid JSON array to your output file (named below). No prose, no markdown fencing, no preamble, no trailing commentary. `[]` is valid and expected when you find nothing — do NOT invent findings to fill a quota.
Each element MUST match this schema exactly:
{
  "source": "<your assigned source value>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the EXACT lines you READ from the file/diff that prove the claim, pasted verbatim. 'N/A' ONLY for findings with no possible code reference. Do not paraphrase; do not reconstruct from memory.>",
  "detail": "<why this is a problem, <=40 words; for acceptance findings quote the violated spec phrase>",
  "recommended_fix": "<the change to apply, <=40 words>"
}"""

ACCURACY = """ACCURACY MANDATE — the most important instruction: NO claim you make will be taken at face value. Every finding will be independently re-verified against the actual worktree before it reaches the report. Findings whose `evidence` cannot be located verbatim, or whose claim contradicts the code, are DISCARDED SILENTLY — no defense, no second chance. Therefore: OPEN the file, READ the cited lines. Quote them verbatim in `evidence`. Hedging ("might", "could", "possibly") signals you have NOT verified — either verify and report crisply, or drop it. Prefer fewer well-grounded findings over many speculative ones. An empty array is an honest, fine answer."""

BRIEFS = {
"blind": """You are a cynical, jaded reviewer with zero patience for sloppy work. BLINDNESS RULE: the diff file is ALL the context you may use. Do NOT read the worktree, the specs, or any other file — reading anything beyond the diff INVALIDATES your lens. Assume problems exist; be skeptical; look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (the comments / commit message)

Your `evidence` MUST be exact diff lines pasted verbatim from the diff file. `source` = "blind".""",

"edge": """You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability, off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing. `source` = "edge".""",

"acceptance": """Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible). `source` = "acceptance".""",

"security": """OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

This is a single-player desktop game with a headless demo/replay harness (Odin) — most OWASP categories will not apply; the realistic surface here is missing validation at the .dem parse boundary (spawn_node coords / type names / fixture values), integer-overflow/coercion at parse, and path handling in golden/report writers. `[]` is an honest answer. `source` = "security".""",

"architecture": """Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns (esp. ODN-1 core/presentation — the harness must stay engine-free-core / tooling-side; ODN-11 replay contract)?
- Will it create technical debt or make future changes harder (later slices add more demo verbs + topology directives)?
- Does complexity match the problem? Any premature abstraction? (NOTE: the Demo_Replay single-struct is a documented deliberate decision — the lens-guards.)

`source` = "architecture".""",

"codebase": """Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match? (pp.node_type_index, pp.topology_spawn_node, seed_fixture, lower_spawns, Session_Cfg, make_drift_mutations, replay_hashes callers — check ALL of them against the worktree)
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.) Does the demo fixture's odin-test opt-out hold (check whether any core/*_test.odin or harness code path still calls the removed load_demo_spawns/load_demo_session)?
- Does it leave orphan code — functions, exports, types no longer referenced after this change? (grep for load_demo_spawns / load_demo_session remnants)

`source` = "codebase".""",

"tests": """Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

The P0 critical paths here: the golden-blessing comparison path (mismatch -> fail, never silent re-bless), spawn_node determinism (same demo text -> same topology, ids = spawn order), the ODN-11 replay gate riding Demo_Replay identically on live + replay paths (a setup piece that drifts = replay divergence), the drift-check still rejecting tampered logs after the load_demo_replay port.

The harness demos ARE the fixture verification here (the demo fixture is deliberately opted out of `odin test` — see the lens-guards; do NOT flag that). But judge whether the NEW code paths (spawn_node parse errors, unknown node type, fixture off + fixture-on mixing, the check_golden allocator fix) are exercised by anything — demos, drift mutations, or not at all.

Blind-spot heuristics to check:
- New/modified behavior without matching coverage
- Happy-path-only coverage where error handling is implied (bad spawn_node lines, unknown type names — are they exercised anywhere?)
- New state transitions without boundary tests

Test level mix: flag mismatches as findings.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100%, P1 ≥90%, overall ≥80%
- CONCERNS: P0 100%, P1 80–89%, overall ≥80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%

`source` = "tests".""",
}

TEMPLATE = """# Perkins lens prompt — @LENS@ (round 1)

**You are the `@LENS@` lens. Your assigned `source` tag is `@LENS@`. Your output file is `@OUTFILE@`.**

You are ONE lens in a Perkins automated PR-review swarm (round 1 of 3). Perkins reviews; lenses find; nobody fixes. You run as a pi agent with read-only access to a git worktree pinned at the reviewed sha.

## Your inputs (READ THESE)
- CANONICAL DIFF (review exactly these bytes): @DIFFPATH@
@WTLINE@@SPECLINE@

## The PR (scope)
@SCOPE@

## ⚠️ CRITICAL lens-guards — READ BEFORE FILING ANYTHING (prevents false positives)
@GUARDS@

## Legitimate findings here WOULD be
@LEGIT@

## OUTPUT CONTRACT (follow exactly)
@CONTRACT@

@ACCURACY@

## YOUR LENS BRIEF

@BRIEF@

## DONE
Write your JSON array to `@OUTFILE@` and stop. Do not fix anything. Do not run the interactive fix flow.
"""

def build(lens):
    outfile = f"{OUT}/{lens}.json"
    if lens == "blind":
        wtline = ""
        specline = ""
    else:
        wtline = f"- WORKTREE (verify every claim against the actual code here — this is your ground truth, detached at sha {SHA}): {WT}\n"
        specline = f"- SPEC / CONTEXT (read the sections named; full files):\n{SPEC_BLOCK}\n"
    t = TEMPLATE
    t = t.replace("@LENS@", lens)
    t = t.replace("@OUTFILE@", outfile)
    t = t.replace("@DIFFPATH@", f"{OUT}/diff.patch")
    t = t.replace("@WTLINE@", wtline)
    t = t.replace("@SPECLINE@", specline)
    t = t.replace("@SCOPE@", SCOPE)
    t = t.replace("@GUARDS@", GUARDS)
    t = t.replace("@LEGIT@", LEGIT)
    t = t.replace("@CONTRACT@", OUTPUT_CONTRACT)
    t = t.replace("@ACCURACY@", ACCURACY)
    t = t.replace("@BRIEF@", BRIEFS[lens])
    return t

os.makedirs(f"{OUT}/prompts", exist_ok=True)
for lens in ("blind", "edge", "acceptance", "security", "architecture", "codebase", "tests"):
    p = f"{OUT}/prompts/{lens}.md"
    with open(p, "w") as f:
        f.write(build(lens))
    print(p, os.path.getsize(p))
