#!/usr/bin/env python3
"""Generate round-2 lens prompts for Perkins routing-forecast-shift fix-audit."""
import pathlib

ROUND = "/Users/moses/code/_bmad-output/perkins/packet-plumber-routing-forecast-shift/r2"
WT = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-routing-forecast-shift-r2"
OUT = pathlib.Path(ROUND) / "lens-prompts"
OUT.mkdir(parents=True, exist_ok=True)

diff = pathlib.Path(f"{ROUND}/diff.patch").read_text()
conventions = pathlib.Path(f"{WT}/project-context.md").read_text()
briefing_c = pathlib.Path("/Users/moses/code/_bmad-output/briefings/packet-plumber-routing-forecast-shift.md").read_text()
briefing_a = pathlib.Path("/Users/moses/code/_bmad-output/briefings/packet-plumber-routing-bandwidth-cost.md").read_text()
canon = pathlib.Path("/Users/moses/code/_bmad-output/problem-solution-2026-08-13.md").read_text()

guards = """=== (round 2 of 3 — fix-audit framing + lens-guards) ===

ROUND CONTEXT: This is Perkins review round 2 on PR #39 (reviewed sha d930de8, base v2).
Round 1 (sha da825d8) found 1 blocker (B1: the acceptance-2 panel path — the U-key
preview rendering — had zero automated coverage), 4 warnings (W1-W4), 6 notes (N1-N6);
the minion pushed a rework commit addressing all of them. Review the diff with fresh
eyes; new findings are welcome, but do NOT re-file a prior finding whose fix is
demonstrably present — read the actual code before filing anything.

LENS-GUARDS (prevents false positives — read before filing):
- LOAD-BEARING — the helper is PURE + honest. (a) The predictive helper is a pure
  function: no state mutation, no rng, integer-only, array-only (ODN-9/10); it RE-RUNS
  Job A's Dijkstra against the HYPOTHETICAL topology (a tier change on one pipe) — the
  prediction must match what the sim WILL do (the honest-prediction pin: apply the
  upgrade FOR REAL in a demo and assert prediction == actual post-upgrade behavior —
  the determinism twin of `expect hash stable`). A prediction that diverges from
  actual post-upgrade routing = a blocker. (b) The helper is a look, NEVER a write —
  no sim-state mutation from the preview path (a write = a blocker).
- LOCKED — do not flag as defects: Job A's Dijkstra model + the splice-proof re-bless
  (settled); `ecmp_pick`/`ecmp_hash`; the table derived-not-serialized; static costs;
  capacity effects (bundle speedups) deliberately out of the helper's path-choice
  scope (the minion flagged this decision); per-class routing preferences (full-game
  idea, scope-guarded out).
- PANEL INTEGRATION: when the player considers upgrading a pipe's tier, the panel
  shows the predicted reroute BEFORE commitment (with the equal-cost split message).
  The wiring must actually consume the helper (a panel that renders but never queries
  = a real defect). The panel shares `app/main.odin` with parallel Job B — review the
  diff at the sha; B's changes are NOT in this PR.
- GOLDEN-DISCIPLINE: NEW golden files only (the property-pin demo); existing goldens
  MUST NOT shift (any shift = a finding — the "STOP and flag" class).
- ODN-5 / scope: no new player commands; LOG_VERSION stays 3 (a bump without a flag =
  flag it); surge/crisis content is settled (4.2 merged — carry-forward only).
- Em-dashes are OK in PP (the RightTenantry ban does not apply).
- Determinism spine reminder: per-hop forwarding, T1 hash rides every serialized
  state, replay byte-identical.
- CI note: GitHub CI is account-billing-blocked (user resolving) — local verification
  at the sha (`odin test core`, harness, drift) is the ground truth for this round.
  You MAY run read-only commands in the worktree to verify claims.
"""

spec = f"""--- SPEC / CONTEXT ---
{briefing_c}
=== (context: Job A's briefing — the capacity-cost routing model this job extends) ===
{briefing_a}
=== (canon: problem-solution-2026-08-13.md — the user ruling driving this job) ===
{canon}
{guards}"""

shared_head = f"""You are reviewing a code diff. You have read-only access to the repository at the worktree path given below and may verify the diff's claims against the actual codebase using your available tools (read files, grep, git show, run read-only commands). You may NOT modify anything in the repository.

WORKTREE (read-only verification target): {WT}
The worktree is checked out at exactly the reviewed sha; trust it over any other checkout.

--- PROJECT CONVENTIONS ---
{conventions}
"""

output_contract = """
--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
"""

lens_briefs = {
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

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).
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
""",
    "architecture": """--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?
""",
    "codebase": """--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?
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

blinds = {
    "blind": """You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

ISOLATION RULE (blindness is your value): you must NOT open the repository, read any other file, run git or grep, or consult any external context — the diff alone is your universe. Reading anything beyond the diff invalidates your lens and your findings will be discarded.

--- DIFF ---
{diff}

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "blind",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact diff lines that prove the claim, pasted verbatim from the diff above. Use 'N/A' only when the claim is about something genuinely absent from the diff (e.g. a missing test file). Paraphrased or reconstructed evidence is hallucination — drop the finding instead.>",
  "detail": "<≤40 words>",
  "recommended_fix": "<≤40 words>"
}

Output contract: ONLY the JSON array. No prose, no fencing, no preamble. `[]` is valid.

ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose `evidence` cannot be located in the diff above, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in `evidence`. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.

FILE-OUTPUT CONTRACT:
- When your analysis is complete, write ONLY your JSON findings array (nothing else — no prose, no markdown) to this EXACT file path: {ROUND}/blind.json
- The file content must be a single valid JSON array, or `[]` if you found nothing.
- After writing the file, send one short message ("done — wrote blind.json") and stop. Do not do any further work.
""",
}

for lens, brief in lens_briefs.items():
    prompt = (
        shared_head
        + f"\n--- DIFF ---\n{diff}\n"
        + spec
        + brief
        + output_contract
        + f"""
FILE-OUTPUT CONTRACT:
- When your analysis is complete, write ONLY your JSON findings array (nothing else — no prose, no markdown) to this EXACT file path: {ROUND}/{lens}.json
- The file content must be a single valid JSON array, or `[]` if you found nothing.
- After writing the file, send one short message ("done — wrote {lens}.json") and stop. Do not do any further work.
"""
    )
    (OUT / f"prompt-{lens}.txt").write_text(prompt)

for lens, prompt in blinds.items():
    prompt = prompt.replace("{diff}", diff).replace("{ROUND}", ROUND)
    (OUT / f"prompt-{lens}.txt").write_text(prompt)

# sanity: every prompt ends with the file-output contract for its own lens
for f in sorted(OUT.glob("prompt-*.txt")):
    n = f.stat().st_size
    ok = f.name.endswith(".txt")
    print(f"{f.name} {n} bytes ok={ok}")
print("done")
