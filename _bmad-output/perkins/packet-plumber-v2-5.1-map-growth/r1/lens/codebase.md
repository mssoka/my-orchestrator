You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- INPUT FILES (read them in this order) ---
1. DIFF: read /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.1-map-growth/r1/diff.patch — this is the canonical diff under review. Review exactly these bytes.
2. PROJECT CONVENTIONS: read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.1-map-growth-r1/project-context.md (the project's code conduct).
3. SPEC / CONTEXT: read /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.1-map-growth/r1/spec-bundle.md (job briefing, story card, architecture refs, and the Perkins lens-guards — honor them; they name the load-bearing invariants and what must NOT be re-litigated).
4. WORKTREE (for verification reads): /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.1-map-growth-r1 — a checkout at exactly the reviewed sha. Cite locations against files in this worktree.

--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Also verify the claimed inventory: the PR claims 27 pre-existing demos byte-identical/unshifted, a new growth.dem with T1+T2 goldens, and goldens/ untouched except new growth goldens — check the actual files in the worktree (goldens/, demos/, data/) match those claims, and that core consts (not balance.json) carry the growth tuning.

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

FILE-OUTPUT CONTRACT (headless mode — overrides any other output instruction about chat):
- Using your file-writing tool, write ONLY your final JSON array to EXACTLY this path (do not derive, do not guess, copy it verbatim):
  /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.1-map-growth/r1/codebase.json
- The file must contain the JSON array and nothing else — no prose, no markdown fencing.
- After writing the file, stop. Your work is done; do not wait for further instructions.