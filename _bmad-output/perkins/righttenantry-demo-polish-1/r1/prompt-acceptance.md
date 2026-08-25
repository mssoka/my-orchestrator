You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- INPUTS ---
- Diff (canonical, review exactly these bytes): /Users/moses/code/_bmad-output/perkins/righttenantry-demo-polish-1/r1/diff.patch — read it first.
- Worktree (checkout at the reviewed sha; ALL verification reads happen here): /Users/moses/.herdr/worktrees/RightTenantry/perkins-demo-polish-1-r1
- Project conventions: AGENTS.md at the worktree root — read it.
- Spec / context docs:
  - /Users/moses/code/_bmad-output/briefings/perkins-righttenantry-demo-polish-1-r1.md (review briefing with lens-guards)
  - /Users/moses/code/_bmad-output/briefings/righttenantry-demo-polish-1.md (original job briefing, the 5+1 fixes spec)

--- OUTPUT ---
Write ONLY a valid JSON array to the file path given below (use the Write tool, full absolute path — do not derive a different path). Each element must match this schema exactly:
{
  "source": "<the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- The file must contain ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, STOP. Print one line confirming the path and finding count.

ACCURACY MANDATE — this is the most important instruction:

NO claim you make will be taken at face value. Every finding will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY.

Therefore:
- Open the file in the worktree. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code.
- The evidence field must contain the EXACT lines you read. A finding without locatable evidence is a hallucination — drop it.
- Hedging language ("might", "could", "possibly") means you have not verified. Either verify and report crisply, or do not report.
- Prefer fewer, well-grounded findings over speculative ones. An empty array is a fine and honest answer.

--- YOUR LENS (source: acceptance) ---
Audit the diff against the spec and context docs (the review briefing lens-guards and the original job briefing 5+1 fixes). Identify: violations of specific acceptance criteria; deviations from spec intent; missing implementation of specified behavior; contradictions between spec constraints and actual code; scope drift. Pay special attention to the 6 fix-audit items: (1) toast parity pin + the #615 consent-banner guarantee intact, (2) Remind + Follow-up must mutate demo row state not just toast, (3) Compare Top 3 pins, (4) demo report detail matches real report structure with demo data, (5) logo/wordmark navigates to landing, (6) zero `grace` grep hits in demo code (a-grainne rename). Also the no-network pillar: demo issues ZERO real API calls. For each finding, quote the violated AC or constraint in detail.

Write the JSON array to: /Users/moses/code/_bmad-output/perkins/righttenantry-demo-polish-1/r1/acceptance.json
