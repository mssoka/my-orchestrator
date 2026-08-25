You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

BEFORE ANYTHING ELSE, use your read tool on these exact paths:
1. The canonical diff (review EXACTLY these bytes — never re-fetch or regenerate the diff): /Users/moses/code/_bmad-output/perkins/packet-plumber-local-ci-suite/r1/diff.patch
2. The spec (the original job briefing): /Users/moses/code/_bmad-output/briefings/packet-plumber-local-ci-suite.md
3. The reviewer lens-guards (read ONLY the section 'Lens guards (round-specific)' plus the PR/sha header): /Users/moses/code/_bmad-output/briefings/perkins-packet-plumber-local-ci-suite-r1.md
4. Project conventions: /Users/moses/.herdr/worktrees/packet-plumber/perkins-local-ci-suite-r1/project-context.md
5. The spec-of-record that the diff must replicate: /Users/moses/.herdr/worktrees/packet-plumber/perkins-local-ci-suite-r1/.github/workflows/ci.yml (the workflow is the spec — it must stay byte-identical to base; the diff must NOT touch it)

All verification reads happen in the worktree at: /Users/moses/.herdr/worktrees/packet-plumber/perkins-local-ci-suite-r1
(It is a checkout at exactly the reviewed sha. Trust it, not any remote branch.)

--- PROJECT CONVENTIONS ---
In /Users/moses/.herdr/worktrees/packet-plumber/perkins-local-ci-suite-r1/project-context.md — read it.

--- DIFF ---
In /Users/moses/code/_bmad-output/perkins/packet-plumber-local-ci-suite/r1/diff.patch — read the whole file. Do not review anything outside those bytes.

--- SPEC / CONTEXT ---
The original job briefing at /Users/moses/code/_bmad-output/briefings/packet-plumber-local-ci-suite.md, plus the lens-guards section of /Users/moses/code/_bmad-output/briefings/perkins-packet-plumber-local-ci-suite-r1.md. The GitHub issue is intentionally absent (USER-ORDERED job). Key guard summary (verify, do not re-litigate):
- The ONE hard blocker: the local suite must implement EVERY gate of .github/workflows/ci.yml with the same failure semantics — the enumeration is 8 gates (lint, odin test core, app.bin build, harness run, drift-check, preview-check, PP_DEBUG builds, stats-check pause+qos_contention), in CI order, stop-on-fail. The workflow file itself must be untouched by the diff.
- Verify specifically: the container leg is a faithful ubuntu replica (pinned Odin from .odin-version, arm64+amd64, the workflow's X11 deps, rlsw shadow baked at build time); artifact isolation (image COPYs the tracked tree, .dockerignore strips bin/, tools/raylib-sw/shadow, goldens/_reports/; only writable host surface is the goldens/_reports bind-mount; a second run must not be poisoned); --windows-cross is compile-only, report + exit 0-with-warning, and MUST detect a missing output binary rather than trusting the exit code; docker-not-running detection is plain-language.
- Do NOT re-litigate: the user ruling itself (local replica, workflow untouched), and the billing doctrine (local suite passing at the sha = ground truth; do not demand GH Actions evidence).
- Flag for verification: the README gate-mapping table must match the actual workflow steps 1:1; .gitignore/.dockerignore changes must be scoped to artifacts only.
- Acceptance evidence in the diff's spec artifact (_bmad-output/implementation-artifacts/spec-local-ci-suite.md) is the implementer's own claim — treat timings/results as claims, review the CODE, and do not penalize the absence of GH Actions runs (billing-blocked; user-ruled doctrine).

--- YOUR LENS ---
OWASP-oriented security review of the diff, scaled to what this diff IS: local dev tooling (a bash script, a Dockerfile, a .dockerignore, docs). Identify:
- Unsafe secret, token, or credential handling (leaks to logs, image layers, committed files — check .dockerignore/.gitignore actually exclude .env and friends)
- Injection vectors: command injection via unquoted expansions in tools/ci-local.sh and Dockerfile.ci (user-controlled vars, paths with spaces, $(...) flows), curl|shell patterns, unsafe tar extraction
- Supply-chain exposure: unpinned base image or unpinned/unverified downloads (curl -fsSL of the odin tarball — is the base image tagged? is there any checksum/signature verification, and does the workflow itself verify? — parity with the workflow is the bar, flag only gaps BEYOND the workflow's own posture)
- Privilege issues: container runs as host uid — any path where root-owned debris lands on the host, or world-writable (a+rwX) surfaces that leak beyond the container
- Docker socket / daemon exposure, host path bind-mounts beyond goldens/_reports
- Data exposure: anything sensitive that would end up inside the built image (the COPY . /src with the .dockerignore as the only guard — walk the exclusion list against what a repo checkout actually contains)

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "security",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

FILE-OUTPUT CONTRACT (mandatory): write ONLY the JSON array (no prose, no markdown fencing) to this exact absolute path using your write tool:
/Users/moses/code/_bmad-output/perkins/packet-plumber-local-ci-suite/r1/security.json
Then stop. Do not print the findings into the chat; the file is the deliverable. An empty array [] written to the file is a valid, honest result.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
