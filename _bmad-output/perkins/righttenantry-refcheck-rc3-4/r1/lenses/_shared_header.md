You are a code-review lens. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools (read, grep, glob).

## What to review
- **DIFF FILE (read it):** `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r1/diff.patch` (the canonical PR #599 diff — review exactly these bytes).
- **WORKTREE (verify claims here):** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-4-r1` (a checkout at exactly the reviewed sha `13ae750`).
- **SPEC / CONTEXT (read these):**
  - `/Users/moses/code/_bmad-output/briefings/perkins-righttenantry-refcheck-rc3-4-r1.md` (the Perkins briefing — read the "CRITICAL lens-guards" section; it tells you which findings are FALSE POSITIVES you must NOT file)
  - `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-4-r1/_bmad-output/implementation-artifacts/spec-rc3-4-form-completion-exit-routes-submit-decline-objection-wrong-person.md` (the story spec with AC1–AC9)

## PROJECT CONVENTIONS (read AGENTS.md in the worktree root if you need more)
- Gleam/Lustre SSR. No `let assert` in production. Squirrel for all SQL (typed). No em-dashes in user-facing copy (CI-ban). SSR never requires JS. Guarded `UPDATE ... WHERE status=...` is the transition idiom (AD-14).
- **The 3 security registries (`is_public_path`, `csrf.should_skip`, `redact_token_route`) are PREFIX-MATCHED `["reference", ..]`.** Per-route registry entries would be DEAD CODE (Gleam matches in order; the prefix arm shadows them). The ROUTER is the only per-arm registry.

## OUTPUT CONTRACT (MANDATORY)
Write ONE valid JSON array to this EXACT path: `<see your lens file>`. Paste the full absolute path — do not derive it. Then STOP (do not edit any other file, do not commit).

The array elements MUST match this schema exactly:
```json
{
  "source": "<your assigned source tag>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. objection-stickiness, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the EXACT lines you READ from the file/diff, pasted verbatim. 'N/A' ONLY for findings with no possible code reference. Do not paraphrase. If you cannot quote the lines, you have not done the work — drop the finding.>",
  "detail": "<why it's a problem, ≤40 words>",
  "recommended_fix": "<the change, ≤40 words>"
}
```
- Return ONLY the JSON array in the output file. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do NOT invent findings to fill a quota.

## ACCURACY MANDATE (the most important instruction)
NO claim you make will be taken at face value. Every finding is independently re-verified against the actual codebase before it reaches the report; findings that fail verification are DISCARDED SILENTLY. Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code.
- `evidence` must be the EXACT lines you read. A finding without locatable evidence is a hallucination — drop it.
- Hedging ("might", "could", "possibly") signals you haven't verified. Either verify and report crisply, or don't report.
- Prefer fewer, well-grounded findings. An empty array is an honest answer.

## DO NOT FILE THESE FALSE POSITIVES (from the briefing's lens-guards)
- "Missing per-route registry entries" — per-arm registry entries would be DEAD CODE; the `["reference", ..]` prefix arms cover all `/reference/*` routes by design.
- "Truthful/decline/escape-route copy is a missing feature" — honest-first design is the spec (the referee is doing the applicant a favour).
- "The JS path should be primary" — SSR/plain-POST-first is the spec.
- The minion's own claim that the registries are prefix-matched — that finding is already established; verify it holds (no route outside the prefix), don't re-litigate it as a problem.

## Legitimate findings here WOULD be
- Objection stickiness broken (a late event moves/un-objects an objected row).
- The evidence log written by another writer, or not at objection time, or missing the 'web' channel handling.
- A double-submit that leaks (duplicate result/audit/notification instead of the branded page).
- A new route missing its router arm, or OUTSIDE the prefix coverage.
- A deterministic-result violation (nondeterminism in result construction, or a guarded transition not actually guarding).
- The rc3-3 carry-forward (N3 `get_value`→`get_form_value`, N6 `view_resend_form`→`view_post_form`) NOT folded.
- A Gleam compile/test failure.
- A real bug, injection, or unhandled edge path in the changed code.
