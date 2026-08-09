#!/usr/bin/env python3
"""Generate lens prompts for the 6 chunks x 7 lenses. Prior-round pattern."""
import os

OUT = "/Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r1"
WT = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-odin-prototype-r1"
PROMPTS = f"{OUT}/prompts"
os.makedirs(PROMPTS, exist_ok=True)

CHUNKS = {
    "a": "chunk-1-core-sim.patch",
    "b": "chunk-2-core-tests.patch",
    "c": "chunk-3-app.patch",
    "d": "chunk-4-harness.patch",
    "e": "chunk-5-goldens.patch",
    "f": "chunk-6-misc.patch",
}

SPEC = f"""--- SPEC / CONTEXT ---
You have read-only access to the repository at {WT} and MUST verify the diff's claims against the actual codebase (read files there). The diff file is the canonical reviewed bytes; the worktree is pinned at the reviewed commit.

Specs (read them):
- Round briefing (Perkins mandate + LENS-GUARD — read first): {OUT}/spec/round-briefing.md
- Job briefing (acceptance): {OUT}/spec/job-briefing.md
- THE CANON SPEC — Odin architecture (ODN-1..18, §10 harness, E1..E32 contracts): {OUT}/spec/odin-architecture-v1.md
- GDD (engine-agnostic design: M1..M5, QoS lanes, crisis model): {OUT}/spec/gdd.md

LENS-GUARD (from the round briefing — prevents false positives; read the full version in the round briefing):
This is an EARLY PROTOTYPE for an engine A/B, not production code. Perkins mandate: "the determinism spine is the ONE hard blocker; otherwise prototype-rigor for the comparison gate, not production-grade."
- Do NOT flag "not production-grade" / "missing full-game features" as blockers (era tree, leaderboard, mobile, save system are deliberately NOT built).
- Do NOT flag Odin/Raylib as "wrong engine" or suggest Godot/GDScript/C# (the pivot is the user's ruling).
- Do NOT flag prototype debt (hardcoded values, stubbed systems, minimal validation) as BLOCKERS — warnings/notes only.
- Do NOT re-litigate the Godot #11 findings (prior round: 46 findings on the merged Godot prototype). Those informed this re-implementation; verify the lessons were APPLIED (e.g. serialization is field-wise canonical, never raw in-memory bytes).
- CI: the `.odin-version` pins `dev-2026-08-nightly` (not a valid upstream branch) so the CI verify job fails to clone Odin — KNOWN issue, do NOT re-flag (note it's known).
Legitimate blocker-class findings: determinism spine compromised (seeded run does not reproduce; sim tangled with raylib; vendor/OS imports in core/; float nondeterminism in sim; unowned PRNG; iteration-order dependence); golden harness fake (tautological compares, raw-bytes T1 hash, false replay claims); core-loop BUG (packets don't flow, QoS priority broken, surge unsurvivable, port limits not enforced, NetworkHealth/Error 404 broken); committed app.bin binary; compile/runtime crash.

Prior-round context (Godot #11, 46 findings — the lessons to verify APPLIED, not re-litigate):
- NetworkHealth win/lose/drain had ZERO test coverage; QoS priority behavior untested
- Upgrade validation charged full tier cost but applied only the delta; span check skipped on upgrade
- Junction demolish left ghost pipes; batch budget could go negative; null-deref in batches
- logic_hz=10 vs ADR-2's 20Hz contradictions; balance never passed to PacketFlow (ms_per_tick stuck at 50)
- Determinism fingerprint OMITTED in-flight packet state + latency (replay-equality could pass while internals diverged) — THE raw-bytes/canonical-form lesson
- Replay-equality keystone ran on a no-pipes topology; submit_command fast-path had an undocumented +1 convention
- Terminal-to-terminal pipes were legal (bypassing routers) — the art-canon rule E26
- QoS emphasis preset was a hardcoded literal, not catalog data; clean_span default read before max_span loaded
- MCPRuntime autoload exposed an unauthenticated TCP control server (security)
- span_between used float sqrt for a state-affecting value

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

You are told this is an Odin + raylib game prototype (a packet-routing puzzle with a deterministic simulation core), but that is ALL you know about the project. Reading anything beyond the diff file invalidates your lens — do not open the worktree or any other file.

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

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.
""",
    "acceptance": """--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible). Priority: the ODN-1/9/10 determinism spine, the §10 golden harness (T1 canonical serialization, T2 software-renderer pixels, replay gate), and the §6 fun-test systems (Topology terminal→router-only E26, PacketFlow, QoS lanes E5-E9, Crisis Surge, NetworkHealth E16/E17, port limits canon #14 basic 4/mid 8/high 16). Also verify the E1-E32 contracts table (§11.7) where the diff touches them. And: was `app.bin` (a compiled binary) committed to the repo? (flag it if so — build artifacts should not be committed). Was `game/` (Godot prototype) removed per the ruling, with the `prototype-fun-gate` tag preserved?
""",
    "security": """--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

(Note: this is a single-player desktop game prototype — adjust expectations; a network listener, shell-out, or path traversal would be notable here. The prior Godot round found an unauthenticated TCP MCP server — check nothing like that exists here.)
""",
    "architecture": """--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

Check against the canon spec's architecture: core/ pure (no vendor/OS imports), snapshot = SOA memcpy contract between core and view, QoS procs inside flow (ODN-3), event buffer ODN-14, arena discipline ODN-18, no globals ODN-13, owned PRNG ODN-9. Flag deviations from these structural rules.
""",
    "codebase": """--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Worktree: {wt}
""",
    "tests": """--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80-89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New/modified API endpoints without matching coverage
- Auth/authz paths missing negative tests
- Happy-path-only coverage where error handling is implied
- New DB operations without integration coverage
- New state transitions without boundary tests

Test level mix (unit/integration/E2E): flag mismatches as findings.

Priority coverage questions for THIS diff: (1) determinism/replay-equality on a REAL topology (the Godot r1 keystone ran on a no-pipes topology — verify the Odin keystone is packet-rich), (2) QoS priority behavior (promote/demote, drop ladder E9, no-starvation E7, largest-remainder E8), (3) NetworkHealth win/lose/drain (P0 — the MVP win condition), (4) node health 🟡/🔴 warning surface, (5) the golden-harness demos (do they exercise the behaviors they claim — surge survivability, QoS dial, error 404?), (6) port limits (canon #14: basic 4/mid 8/high 16), (7) upgrade validation (tier-delta cost + span check — the Godot r1 gaps), (8) terminal-to-terminal rejection (E26), (9) log round-trip + corrupt-log rejection (ODN-11).

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100%, P1 ≥90%, overall ≥80%
- CONCERNS: P0 100%, P1 80-89%, overall ≥80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%
""",
}

OUTPUT_CONTRACT = """
--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
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
- Write ONLY the JSON array to: {outfile}. No prose, no markdown fencing, no preamble in the file.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, finish with one line in the pane: "{lens} done: N findings".

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
"""

for chunk, fname in CHUNKS.items():
    diff_path = f"{OUT}/{fname}"
    for lens in ["blind", "edge", "acceptance", "security", "architecture", "codebase", "tests"]:
        outfile = f"{OUT}/{lens}-{chunk}.json"
        if lens == "blind":
            prompt = BLIND_TEMPLATE.format(diff=diff_path, outfile=outfile)
        else:
            prompt = SHARED_HEAD.format(spec=SPEC, diff=diff_path) + LENSES[lens] + OUTPUT_CONTRACT.format(lens=lens, outfile=outfile)
        if lens == "codebase":
            prompt = prompt.replace("{wt}", WT)
        with open(f"{PROMPTS}/{lens}-{chunk}.md", "w") as f:
            f.write(prompt)
        print(f"{lens}-{chunk}.md written -> {outfile}")
print("done")
