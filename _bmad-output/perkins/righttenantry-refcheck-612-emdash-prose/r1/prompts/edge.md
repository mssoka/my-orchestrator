You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

WORKTREE (verification reads happen here): /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-612-emdash-prose-r1
DIFF FILE (canonical bytes under review — read it in full first): /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-612-emdash-prose/r1/diff.patch
SPEC FILES: /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-612-emdash-prose/r1/issue-612.json and /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-612-emdash-prose/r1/job-briefing.md
PROJECT CONVENTIONS: /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-612-emdash-prose/r1/prompts/conventions.md

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), unhandled error paths in new code, state the new code doesn't account for, input the new code doesn't validate. This PR is a copy-string + lint change: focus on the new `has_em_dash()` scanner (escape-sequence detection, backslash-run parity, span offsets), the removed exemption mechanism (any string that previously rode an exemption and still carries U+2014 would now fail — verify none do), the expanded LINT_SCOPE globs, and the new copy-test scan lists (do they actually cover every re-composed string? which strings fall outside every scan list?).

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<assigned source value>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- Write ONLY your JSON array to the file: /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-612-emdash-prose/r1/edge.json
- No prose, no markdown fencing, no preamble, nothing else in the file.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- When finished writing the file, reply with exactly: LENS DONE

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output.
- Hedging language ("might", "could", "possibly") is a signal you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. An empty array is a fine and honest answer when nothing is wrong.

SCOPE GUARDS (read carefully — these prevent false positives; verified baseline facts, do NOT file findings against them):
- BASE = develop. PR #614 fixes issue #612 ONLY (em-dash copy re-composition + lint exemption removal). RC4.1-4.4, #607, #610 are settled and merged — do not re-open those findings.
- Sibling job #611 (panel-persist) runs in PARALLEL and is NOT part of this PR — do not flag its absence.
- The issue mandates (fix list): reword the 16 inventory strings; remove the SPEC_VERBATIM_OWNERS exemption mechanism; update pinned copy tests; sweep other public surfaces (the lint-scope extension to document_upload.gleam / document_download_page.gleam is the mandated sweep — the em-dash removals in document_upload.gleam are a direct consequence, NOT scope drift).
- The spec-verbatim rewrites are DRAFTS in the issue ("final wording follows brand voice") — the PR may adjust wording beyond a mechanical dash substitution IF meaning + brand voice are preserved and the string stays dash-free. The issue's own suggested rewrite for refcheck_state_failed is "The check hit a problem on our side. It's not {first_name}'s fault." — exactly what the PR ships.
- `.gitignore` `scripts/__pycache__/` is housekeeping for running the Python lint locally — trivial, not a finding.
- GitHub CI is account-billing-blocked — CI redness is NOT a code failure. Local verification at the sha is ground truth.
