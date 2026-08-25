You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

WORKTREE (verification reads happen here): /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-612-emdash-prose-r1
DIFF FILE (canonical bytes under review — read it in full first): /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-612-emdash-prose/r1/diff.patch
SPEC FILES: /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-612-emdash-prose/r1/issue-612.json and /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-612-emdash-prose/r1/job-briefing.md
PROJECT CONVENTIONS: /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-612-emdash-prose/r1/prompts/conventions.md

--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80-89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- The re-composed strings — is EVERY one pinned by a test (the no_em_dash_test scan lists + the verbatim pin tests + the UI render tests)? Which of the 15 former exemptions has NO pin anywhere?
- The lint's new escape-sequence detection (has_em_dash, the Gleam \u{2014} escape form) — is there a negative-control test proving a Gleam source file carrying the escape form fails the lint? And the old raw-form negative controls?
- The exemption-removal property — does any test fail if an em-dash is injected into a formerly-exempt owner (proving the exemption is truly gone)?
- Is there a test for the lint at all (scripts/lint_em_dash.py test harness), or does CI run it bare?
- Renamed tests — do the new names get discovered by gleeunit?

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
- Write ONLY your JSON array to the file: /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-612-emdash-prose/r1/tests.json
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
