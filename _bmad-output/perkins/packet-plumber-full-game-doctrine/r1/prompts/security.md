You are reviewing a DOCS-ONLY diff (no code). You have read-only access to the repository and may verify the diff's claims against the actual files using your available tools. Do NOT modify any file in the repository.

--- PROJECT CONVENTIONS ---
This is a game project (Packet Plumber, Odin + raylib) whose canon lives in planning docs under `_bmad-output/planning-artifacts/`. The established canon-amendment pattern: the decision log is APPEND-ONLY; superseded lines are never struck silently — each carries a dated supersede note citing the decision-log entry that supersedes it. This PR must be docs-only: no code, catalog, balance, golden, or CI-workflow changes.

--- DIFF ---
Read the canonical diff FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-full-game-doctrine/r1/diff.patch (427 lines, unified format, PR #61 of solarity-services/Packet-Plumber, base branch v2). These exact bytes are the review target — never re-fetch or regenerate the diff.

--- WORKTREE (your verification source) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-full-game-doctrine-r1 — a checkout at exactly the reviewed sha (ddf8f2800ac6e7d6fa6331c044aa73447d90a513). Every verification read happens here. Trust this checkout, not origin/v2.

--- SPEC / CONTEXT ---
- Job briefing (the spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-full-game-doctrine/r1/spec/job-briefing.md
- Round briefing (review rulings): /Users/moses/code/_bmad-output/perkins/packet-plumber-full-game-doctrine/r1/spec/round-briefing.md — the r1 guards section is binding on your judgments.
- No GitHub issue exists for this job — the files above are the complete spec.

--- LENS-GUARDS (round-specific rulings — prevents false positives; honor them) ---
THE ONE HARD BLOCKER CLASS for this round is canon consistency + provenance discipline (owned by other lenses). YOUR blocker class is narrower:
- Any non-docs file in the diff (code, catalog/balance JSON, goldens, CI workflow, scripts) = blocker (scope violation).
- Any secret, credential, token, private key, or personal data introduced into the docs = blocker.
WHAT NOT TO RE-LITIGATE (false-positive guards — do NOT file these):
- The user ruling itself; the lavish-approved amendment set; the 5.5/7.2 stories; the fun-test gate's existence; the pre-existing "PR open, in review" 5.5 status line in stories-v2.md (note-only).
- Quoted user-ruling text and quoted superseded framing inside dated supersede notes — intentional provenance, not leakage of anything sensitive.
- GitHub usernames/org names already public in the repo (solarity-services, PR references like #17/#59/#60) — not sensitive.
- GitHub Actions being org-billing-blocked on #61 is NOT a signal (docs-only PR).

--- YOUR LENS ---
Security review of a docs-only diff. Identify:
- Secrets/credentials/tokens/keys/passwords introduced anywhere in the diff
- Personally identifiable information beyond already-public project references (real names, emails, addresses)
- Any non-docs file touched by the diff (scan EVERY `diff --git` header — the diff must contain exactly five paths, all under `_bmad-output/planning-artifacts/`)
- Executable content smuggled into docs (shell commands with side effects, curl-pipe patterns, embedded scripts) presented as instructions a reader might run
- Links introduced by the diff pointing outside known project/GitHub domains

Your `source` value is "security".

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "security",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. secret, pii, scope-violation>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:
NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual files before it reaches the report. Findings that fail verification are DISCARDED SILENTLY. Open the file. Read the relevant lines. The `evidence` field must contain the EXACT lines you read. Hedging language ("might", "could", "possibly") is a signal that you have not verified — either verify and report crisply, or do not report. Prefer fewer, well-grounded findings. An empty array is a fine and honest answer.

FILE-OUTPUT CONTRACT (headless mode): using your file-write tool, write ONLY your JSON array (valid JSON, no prose, no markdown fencing, no preamble) to exactly this absolute path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-full-game-doctrine/r1/security.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens security complete — N findings written".
