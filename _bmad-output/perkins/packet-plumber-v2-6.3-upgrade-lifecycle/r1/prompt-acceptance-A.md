You are reviewing a code diff. You have read-only access to the repository (worktree: /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-6.3-upgrade-lifecycle-r1) and may verify the diff's claims against the actual codebase using your available tools. NEVER modify any file in the worktree; NEVER run git commands that change state (no commit/checkout/push). This is chunk A of a chunked review: all source changes — core/, app/, harness/, demos/, data/, docs/canon, .memlog.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-6.3-upgrade-lifecycle-r1/project-context.md — the project's code conduct. Follow it as the conventions baseline.

--- DIFF ---
The exact diff bytes under review are saved at: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-6.3-upgrade-lifecycle/r1/chunk-A-source.patch
Read that file FIRST — every finding must be grounded in those bytes and verified against the worktree.

--- SPEC / CONTEXT ---
Read these spec documents (in order):
1. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-6.3-upgrade-lifecycle/r1/pr-body.md — the PR's own claims, decisions + rationale (the takeover handoff).
2. /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-6.3-upgrade-lifecycle.md — the original job briefing (mission, deliverables, acceptance criteria, scope guard).
3. /Users/moses/code/_bmad-output/briefings/perkins-packet-plumber-v2-6.3-upgrade-lifecycle-r1.md — the review round briefing (lens-guards: what is a blocker class, what NOT to re-litigate, what to flag).

--- REVIEW GUARDS (Perkins round context — read the briefing for detail) ---
- ONE hard blocker class: the determinism/replay spine + the decay measurability contract. Legacy decay must be DETERMINISTIC and MEASURABLE (integer-only, catalog-driven; routing/drop behavior reflects reduced effective capacity — NEVER a view-only illusion).
- Do NOT re-litigate: the landed 6.1/6.2 infra (eras.json, advance gate, legacy predicate seam — APPROVED rounds); the draw-era tracking REJECTION (GDD M1 + the blessed 6.2 goldens pin the tier predicate — you may verify the argument holds, not re-open it); user rulings (loop-until-APPROVED, canon M4 boundary); fold-forward items already applied from 6.2's rounds.
- FLAG for verification: the re-pinned fixtures' honesty (a fixture re-pin can hide a behavior regression); LOG_VERSION 6 header discipline; the golden contrast legacy_decay vs legacy_modernized (identical seed/topology/demand, one modernizing at the fire — the T1 contrast must be REAL).
- CI is billing-blocked on GitHub; the local suite is ground truth.

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

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
- Write ONLY your JSON array to the file named below (create/overwrite it; nothing else in the file), then STOP.
- The file must contain ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
Your output file (write your JSON array here, then stop): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-6.3-upgrade-lifecycle/r1/acceptance-A.json

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.