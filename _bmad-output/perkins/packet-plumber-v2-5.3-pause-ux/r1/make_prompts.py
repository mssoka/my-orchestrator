#!/usr/bin/env python3
"""Assemble the 7 Perkins lens prompts (headless mode) — verbatim skill structure."""
import json, pathlib

R1 = pathlib.Path("/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.3-pause-ux/r1")
WT = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.3-pause-ux-r1"
diff = (R1 / "diff.patch").read_text()
conventions = pathlib.Path(WT + "/project-context.md").read_text()
issue = json.load(open(R1 / "issue-48.json"))
issue_txt = f"# GitHub issue #{48} (THE SPEC — the user report IS the spec)\n\n## Title\n{issue['title']}\n\n## Body\n{issue['body']}\n"
job_brief = pathlib.Path("/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-5.3-pause-ux.md").read_text()
# lens-guards: extract from the Perkins round briefing
rb = pathlib.Path("/Users/moses/code/_bmad-output/briefings/perkins-packet-plumber-v2-5.3-pause-ux-r1.md").read_text()
start = rb.index("## ⚠️ CRITICAL lens-guards")
end = rb.index("## Standing orders")
guards = rb[start:end].strip()

SPEC = f"""--- SPEC 1: GitHub issue #48 (authoritative — the user report IS the spec) ---
{issue_txt}

--- SPEC 2: original job briefing ---
{job_brief}

--- REVIEW GUARDS from the Perkins round briefing (binding context — prevent false positives; do not re-litigate settled rulings) ---
{guards}
"""

SCHEMA = """{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}"""

OUTPUT_CONTRACT = """--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
""" + SCHEMA + """

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

FILE_OUTPUT = """

--- HEADLESS FILE-OUTPUT CONTRACT (overrides the in-reply output above) ---
You are running headless as a mega-minion pane. When done:
1. Write your JSON array (and NOTHING else — no prose, no fencing) to EXACTLY this absolute path: {out_path}
   (use your file-writing tool; create the file, do not derive any other path).
2. Reply with a single line: DONE <lens>.
3. Stop. Do not fix anything, do not run tests beyond what your lens needs, do not spawn anything.
"""


def shared(lens_brief, out_path, source):
    return f"""You are reviewing a code diff. You have read-only access to the repository at {WT} (a detached checkout at exactly the reviewed sha — verify every claim there) and may verify the diff's claims against the actual codebase using your available tools. Your `source` value is: {source}.

--- PROJECT CONVENTIONS ---
{conventions}

--- DIFF (the canonical diff — review exactly these bytes) ---
{diff}

--- SPEC / CONTEXT ---
{SPEC}

--- YOUR LENS ---
{"".join(lens_brief)}

{OUTPUT_CONTRACT}{FILE_OUTPUT.format(out_path=out_path, lens=source)}"""


LENS_BRIEFS = {
    "edge": """You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.""",
    "acceptance": """Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).""",
    "security": """OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps""",
    "architecture": """Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?""",
    "codebase": """Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?""",
    "tests": """Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
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
- CONCERNS: P0 100%, P1 80–89%, overall ≥80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%""",
}

for lens, brief in LENS_BRIEFS.items():
    p = R1 / f"prompt-{lens}.md"
    p.write_text(shared(brief, str(R1 / f"{lens}.json"), lens))
    print(lens, len(p.read_text()))

# blind hunter — isolated: diff only, no conventions/spec/worktree
blind = f"""You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

You are running headless. You have tools, but your lens is BLIND BY DESIGN: reading any file beyond this prompt invalidates your lens — the diff below is your entire universe. Do NOT read the repository, do NOT open files, do NOT run commands. Judge ONLY the bytes below.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

--- DIFF ---
{diff}

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{SCHEMA.replace('<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>', 'blind')}

Output contract: ONLY the JSON array. No prose, no fencing, no preamble. `[]` is valid.

ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose `evidence` cannot be located in the diff above, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in `evidence`. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.
{FILE_OUTPUT.format(out_path=str(R1 / 'blind.json'), lens='blind')}"""

(R1 / "prompt-blind.md").write_text(blind)
print("blind", len(blind))
