You are reviewing a code diff. You have read-only access to the repository at /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.3-accessibility-core-r3 (a detached checkout at exactly the reviewed state) and may verify the diff's claims against the actual codebase using your tools. Your cwd IS that worktree.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.3-accessibility-core-r3/project-context.md (the project's conduct rules — Odin + raylib, golden-image harness, ODN citation tags). Key invariants: sim is pure/deterministic (ODN-1: the sim NEVER sees presentation state; view-reads-snapshot); presentation changes live only in app/ (view lane); goldens are blessed via the harness; input parity mouse==touch==controller (ODN-12).

--- DIFF ---
The canonical diff for this review chunk is the file: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r3/chunk-app.patch (2295 lines, unified format). Read the WHOLE file first (use offset/limit to page through it). Review exactly these bytes.

--- SPEC / CONTEXT ---
Read these spec files:
1. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r3/pr_body.md — the PR body (the implementer's claims; the r2→r3 section at the end describes this round's fixes)
2. /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-7.3-accessibility-core.md — the original job briefing (the spec: deliverables + acceptance)
3. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r3/lens-guards.md — round-specific review guards (what is a hard blocker vs prototype-rigor; what NOT to re-litigate)

--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions? (the project's popover/single-source-rect patterns, the pulse_read motion seam, hud() scaling single-source)
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries (view lane vs sim) and separation of concerns?
- Will it create technical debt (hand-synced twins/duplicates are the known debt class here)?
- Does complexity match the problem?

--- OUTPUT ---
Write ONE valid JSON array to the file /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r3/architecture-app.json (use your write tool with that EXACT absolute path — do not derive or alter it). Each element must match this schema exactly:
{
  "source": "architecture",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. boundary, coverage-gap, scaling>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- The file /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r3/architecture-app.json must contain ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — the most important instruction:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output.
- Hedging language ("might", "could", "possibly") is a signal you have not verified. Either verify and report crisply, or do not report.
- Prefer fewer, well-grounded findings over speculative ones. An empty array is honest when nothing is wrong.

After writing the file, your final message is just: done