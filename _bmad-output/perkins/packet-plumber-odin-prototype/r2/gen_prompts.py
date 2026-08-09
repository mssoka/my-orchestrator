#!/usr/bin/env python3
"""Generate lens prompts for r2: 7 chunks x 7 lenses (r1 pattern, r2 lens-guard)."""
import os

OUT = "/Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r2"
WT = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-odin-prototype-r2"
PROMPTS = f"{OUT}/prompts"
os.makedirs(PROMPTS, exist_ok=True)

CHUNKS = {
    "a": "chunk-1-core-sim.patch",
    "b": "chunk-2-core-tests.patch",
    "c": "chunk-3-app.patch",
    "d": "chunk-4-harness.patch",
    "e": "chunk-5-goldens.patch",
    "f": "chunk-6-game-removal.patch",
    "g": "chunk-7-misc.patch",
}

SPEC = f"""--- SPEC / CONTEXT ---
You have read-only access to the repository at {WT} and MUST verify the diff's claims against the actual codebase (read files there). The diff file is the canonical reviewed bytes; the worktree is pinned at the reviewed commit (ea678a8).

Specs (read them):
- Round briefing (Perkins mandate + LENS-GUARD — read first): {OUT}/spec/round-briefing.md
- Job briefing (acceptance): {OUT}/spec/job-briefing.md
- THE CANON SPEC — Odin architecture (ODN-1..18, §10 harness, E1..E32 contracts): {OUT}/spec/odin-architecture-v1.md
- GDD (engine-agnostic design: M1..M5, QoS lanes, crisis model): {OUT}/spec/gdd.md

THIS IS ROUND 2 (fix-audit). Round 1 reviewed sha 0118cc0 and posted CHANGES_REQUESTED; Perkins has already personally audited every r1 finding against the worktree. The r1 blockers (committed app.bin; UI-dead demolish) are CONFIRMED FIXED — do not re-report them. These r1 findings are CONFIRMED STILL PRESENT — do NOT re-report them either (they are carried forward by Perkins; your budget is for NEW issues):
- E7 WRR-floor test still vacuous (weights {{100,1,1}} > MAX_WEIGHT=64 silently rejected; submit_c discards the error)
- severance-reroute test still can't distinguish reroute-survival from fresh spawns (`_ = sev_drops_before`)
- harness `save` still blesses failed demos (`return ok || save`)
- harness demo_parse 'demolish node' with no name still indexes fields[2] OOB
- crises.json parsed but never consumed; jint i64->i32 truncation + unknown keys accepted
- zero-traffic neutral ticks still drain at max severity mid-breach (health.odin:73)
- pick_dst still allocates two dynamic arrays per spawned packet on the run arena
- grace countdown in the HUD still computes ticks*hz, discards it, draws a static "!"
- grace-reset test still can't distinguish gradual refill from instant re-arm
- draw_and_reject.dem header still overclaims (and now references the REMOVED budget system)
- nearest_pipe bezier hit-testing still untested; committed r1 review docs still stale
- note-level: dead symbols (state_dump, PCG32_INC, TICK_SECONDS), write_file/write_log dup, raylib tag pin, replay bare=false, rng-test name, tier_by_name dropped ok, app.mode dead, catalog jarr leaks

LENS-GUARD (from the round briefing — prevents false positives; read the full version in the round briefing):
- The determinism spine is the ONE hard blocker: a seeded run MUST reproduce byte-identical T1 state-hash + T2 pixel goldens cross-platform. Perkins has empirically verified it at ea678a8 on macOS (7/7 demos green, replay 3000/3000 bit-for-bit) and CI is green on ubuntu — flag it ONLY if you find a concrete NEW compromise in the diff (e.g. a new float-contraction path the -ffp-contract=off fix misses, an unhashed state field, map iteration, unowned RNG).
- Do NOT re-litigate USER RULINGS: the Mini-Motorways hardware inventory replacing the budget (0b92fa4), desktop-first launch, mouse-only prototype, root layout, the Odin/Raylib pivot, the Godot game/ removal. Review their CORRECTNESS, never their existence.
- Do NOT re-litigate the Godot #11 findings; verify lessons APPLIED.
- Prototype-rigor, not production-grade: missing full-game features (era tree, leaderboards, mobile, save system) are NOT defects. Prototype debt is warning/note, never blocker.
- NEW since r1 — hunt here especially: the hardware-inventory system (Inventory slices on Run_State; validate/apply move stock; Cmd_Place_Router; tick-scheduled grants; Ev_Stock_Arrived; action-log tag 7; tray HUD; autopilot port-reserve/midpoint relay chains), the crash fixes (hint buffer, allocator ownership, MSAA drop + --soak), the -ffp-contract=off T2 fix, the new tests (node-health, queue-overflow), the CI rework (Odin release-tarball install, gdb fallback, per-arch vendor dirs).
Legitimate blocker-class findings: determinism spine compromised (seeded run does not reproduce; sim tangled with raylib; vendor/OS imports in core/; float nondeterminism in sim; unowned PRNG; iteration-order dependence); golden harness fake (tautological compares, raw-bytes T1 hash, false replay claims); core-loop BUG (packets don't flow, QoS broken, surge unsurvivable, inventory stock goes negative / placement bypasses stock, NetworkHealth/Error404 broken); committed binary; compile/runtime crash.

PROJECT CONVENTIONS (from project-context.md, redone for Odin in this branch):
- core/ imports ONLY whitelisted core:* packages — never vendor:*, never core:os, never core:time (ODN-1; CI compile-checked)
- Integer-only sim paths (ODN-10); floats only in the view, never flow back into state
- Never iterate a map in core (map order unspecified) — arrays/slices/#soa only; maps are lookup-only
- RNG is owned (splitmix64→PCG32 XSH-RR, pinned vectors) — never core:math/rand for sim
- Arena discipline (ODN-18): no new/make without an explicit allocator in core
- No globals/singletons (ODN-13); events not callbacks (ODN-14); errors are values (typed enums, no dropped returns)
- Save/log is binary little-endian versioned (ODN-11); JSON only for catalogs, loaded once, fail-fast validated
- Balance numbers live in data/*.json, never literals
- Odin stdlib naming: types/consts Ada_Case, procs/vars snake_case
- Harness (ODN-17): T1 = per-tick FNV-1a-64 of canonical serialized state (field-wise LE, lengths-not-capacities, no padding, includes rng state + event stream); T2 = pixel goldens via rlsw software renderer + PLATFORM_MEMORY, zero-tolerance compare
"""

BLIND_TEMPLATE = """You are a cynical, jaded reviewer with zero patience for sloppy work. The diff file below is ALL the context you have — no project files, no spec, no worktree access. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

You are told this is an Odin + raylib game prototype (a packet-routing puzzle with a deterministic simulation core), round 2 of review (round 1's fixes landed; new code since: a hardware-inventory economy replacing a money budget, crash fixes, a cross-platform float-contraction fix for pixel goldens, new tests), but that is ALL you know about the project. Reading anything beyond the diff file invalidates your lens — do not open the worktree or any other file.

Your diff file: {diff}

Write ONLY the JSON array (schema below) to: {outfile}

## OUTPUT
Return ONE valid JSON array. Each element must match this schema exactly:
{{
  "source": "blind",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact diff lines that prove the claim, pasted verbatim from the diff file above. Use 'N/A' only when the claim is about something genuinely absent from the diff (e.g. a missing test file). Paraphrased or reconstructed evidence is hallucination — drop the finding instead.>",
  "detail": "<<=40 words>",
  "recommended_fix": "<<=40 words>"
}}

Output contract: ONLY the JSON array written to {outfile}. No prose, no fencing, no preamble in the file. [] is valid. After writing, finish with one line in the pane: "blind done: N findings".

ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose evidence cannot be located in the diff, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in evidence. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.
"""

SHARED_HEAD = """You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools (read files under the worktree path below). The diff file is the canonical reviewed bytes.

{spec}

--- DIFF ---
Your diff file (read it fully): {diff}

"""

LENSES = {
    "edge": """--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

Round-2 hotspots to walk especially hard: inventory stock arithmetic (draw/upgrade/demolish/place/grants — can any path drive a count negative or double-return?), Cmd_Place_Router bounds/separation, the action-log tag-7 read/write symmetry, the --soak autopilot loop, grant ticks vs run length.
""",
    "acceptance": """--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible). Priority: the ODN-1/9/10 determinism spine, the §10 golden harness (T1 canonical serialization, T2 software-renderer pixels, replay gate), the E1-E32 contracts table (§11.7) where the diff touches them, port limits (canon #14). Round-2 specifics: does the hardware-inventory implementation keep the determinism contracts (inventory in the T1 hash, grants tick-deterministic, replay tag-7 round-trip)? Does the Godot game/ removal leave any dangling reference (docs, CI, scripts)? Is the -ffp-contract=off fix applied to ALL software-rendered float paths? Do the re-blessed goldens match the new fingerprint fields?
""",
    "security": """--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Missing input validation at system boundaries (demo parser, catalog loader, action-log reader)
- Unsafe secret, token, or credential handling
- Data exposure (sensitive fields in responses, logs)
- Injection vectors (command, path traversal — demo names into paths)
- Unsafe deserialization, insecure defaults
- Supply chain: the raylib fetch (tag vs sha), the CI Odin tarball fetch (checksum?)

(Note: this is a single-player desktop game prototype — adjust expectations; a network listener, shell-out, or path traversal would be notable here.)
""",
    "architecture": """--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

Check against the canon spec's architecture: core/ pure (no vendor/OS imports), snapshot contract between core and view, QoS procs inside flow (ODN-3), event buffer ODN-14, arena discipline ODN-18, no globals ODN-13, owned PRNG ODN-9. Round-2: the Inventory design (slices-views on run-owned arrays threaded through validate/apply), the router-placement flow (tray -> placement mode -> Cmd_Place_Router), the autopilot's port-reserve + relay-chain logic (app-side policy vs core sim), the --soak mode wiring. Flag deviations from the structural rules.
""",
    "codebase": """--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Round-2: the budget->inventory rename — are there leftover budget references (symbols, comments, docs, HUD strings, demo headers) now orphaned by the ruling? Does the game/ removal orphan anything on main (docs referencing game/, the prototype-fun-gate tag story)? Does the CI reference paths that exist?

Worktree: {wt}
""",
    "tests": """--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80-89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New/modified behavior without matching coverage
- Happy-path-only coverage where error handling is implied
- New state transitions without boundary tests

Priority coverage questions for THIS round: (1) the hardware inventory — stock consume/return/exchange, Out_Of_Links / Out_Of_Routers rejections, grants landing, place-router validation (bounds, separation, stock), inventory in replay/determinism; (2) Cmd_Place_Router E2E (a demo?); (3) the autopilot port-reserve + relay chains (any test?); (4) --soak mode; (5) Ev_Stock_Arrived event assertions; (6) the new node-health + queue-overflow tests — read them: are they REAL pins (assert transitions/orders/events) or tautologies? (7) action-log tag-7 round-trip coverage.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS -> note, CONCERNS -> warning, FAIL -> blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100%, P1 >=90%, overall >=80%
- CONCERNS: P0 100%, P1 80-89%, overall >=80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%
""",
}

OUTPUT_CONTRACT = """
--- OUTPUT ---
Write ONE valid JSON array to {outfile}. Each element must match this schema exactly:
{{
  "source": "{lens}",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}}

Output contract:
- The file {outfile} must contain ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, finish with one line in the pane: "{lens} {chunk} done: N findings".

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
"""

for chunk_letter, chunk_file in CHUNKS.items():
    diff = f"{OUT}/{chunk_file}"
    # blind
    out = f"{OUT}/blind-{chunk_letter}.json"
    with open(f"{PROMPTS}/blind-{chunk_letter}.md", "w") as f:
        f.write(BLIND_TEMPLATE.format(diff=diff, outfile=out))
    for lens, brief in LENSES.items():
        out = f"{OUT}/{lens}-{chunk_letter}.json"
        body = SHARED_HEAD.format(spec=SPEC, diff=diff) + brief + OUTPUT_CONTRACT.format(outfile=out, lens=lens, chunk=chunk_letter)
        body = body.replace("{wt}", WT)
        with open(f"{PROMPTS}/{lens}-{chunk_letter}.md", "w") as f:
            f.write(body)

print(f"generated {len(CHUNKS) * 8} prompts in {PROMPTS}")
