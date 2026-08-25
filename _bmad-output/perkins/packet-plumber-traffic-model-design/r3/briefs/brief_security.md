# Lens brief — SECURITY (mm-security-r3) — Perkins round 3, PR #53

## Mechanics

- You are one lens in a headless review wave (Perkins round 3 — FINAL automated round, PR #53 — docs/canon). Work ALONE. Never ask questions; never wait for input. Make reasonable reads yourself and finish.
- Canonical diff (read it FIRST, review exactly these bytes, never re-fetch or regenerate): `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r3/diff.patch` (unified, 1697 lines vs `v2` — 4 markdown canon docs + surge-explainer.html + 3 PNGs, all additions).
- Verification worktree (read-only; detached at exactly the reviewed sha 42e4eb6 — trust it, not origin/v2): `/Users/moses/.herdr/worktrees/packet-plumber/perkins-pp-traffic-model-design-r3`
- Round-2 prior findings: `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r2/consolidated.json` (r2 security lens returned one note: the artifact's sole innerHTML sink — N12, not claimed fixed; expect it carried).
- When done: write ONLY your JSON array to the output path in the OUTPUT CONTRACT section, then stop.

## PROJECT CONVENTIONS

- Repo: Packet Plumber — an internet-building puzzle game (Odin + raylib). This PR is a **design-canon docs PR**: spec + story cards + GDD amendment + decision-log entry + one committed provenance artifact (surge-explainer.html + 3 PNGs, the approved r1-W3 fix). **Scope guard: design docs + story cards ONLY — code, balance.json, and implementation are the story cards' jobs, NOT this PR's.**
- Determinism spine: all rng from `state.rng`, seed-derived, no wall-clock; **ODN-10 integer-only state paths**.
- Coordination constraint: GDD edits must be SECTION-ADDITIVE (no terminology rewrites — the p1P8 terminology audit owns wording and serializes behind this PR).

## LENS-GUARDS — read before reporting (prevents false positives)

This is **round 3 of 3 — the FINAL automated round, a FIX-AUDIT on the r2 rework**. Round 2 verdicted NEEDS CHANGES (1 blocker + 6 warnings + 13 notes); this push claims the blocker + all 6 warnings + notes N1/N5/N8/N9/N11 fixed. Prior findings: `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r2/consolidated.json` (read it).

- **Fix-audit mandate:** where a claimed fix touches your lens, verify it BITES. Do NOT re-report a verified-fixed item as new. Report still-present items with `"still present since round 2"` in the detail, at their r2 severity.
- **Do NOT re-litigate (settled in r1/r2):** committing the surge-explainer html/PNGs (approved provenance artifacts — the r2 N11 provenance disclaimer now marks the exhibit historical); the ~1,000× unit compression; card-format conventions.
- **NOT defects:** the artifact's own superseded §B numbers (spec brackets + supersedes them; provenance disclaimer added); future-tense test pins.
- **Base = `v2`** — the diff is the full PR against v2. Prior-round notes that remain unfixed are carried forward as notes — do not escalate them to blockers.
- **Final-round precision:** a genuine BLOCKER = an actual exploitable vector or committed secret. Safe-only-by-data-flow structure = note (the r2 N12 precedent).

## YOUR LENS

OWASP-oriented security review of the diff. This is a docs/canon PR (markdown + one committed HTML artifact with inline JS + 3 PNGs). Identify:
- XSS/injection vectors in the committed HTML/JS (it is opened locally in a browser — check the JS for eval/innerHTML/document.write on non-constant data, unescaped interpolation)
- Committed secrets, tokens, credentials, or private paths/information in the artifact or docs
- Supply-chain shape of the artifact (external script/font/network fetches, tracking pixels)
- Anything in the docs that instructs insecure practices

Empty array `[]` is a fine and honest answer for a docs PR — round 1's security lens returned exactly that. Do not invent findings.

## OUTPUT CONTRACT

Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "security",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

- Write ONLY the JSON array to your assigned output path (below) — no prose around it in the file — then STOP.
- Empty array `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota.

ACCURACY MANDATE — the most important instruction in this brief:

NO claim you make will be taken at face value. Every finding will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY.

- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly") signals you have not verified. Either verify and report crisply, or do not report.
- Prefer fewer, well-grounded findings over many speculative ones. An empty array is an honest answer.

Your output path: `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r3/security.json`
