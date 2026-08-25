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
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (docker daemon down, network fetch failing, apt failing, the pinned odin tarball 404ing), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For THIS diff specifically trace: every flag combination of tools/ci-local.sh (--fast/--mac/--native/--windows-cross/--in-container/unknown/garbled), the run_gates stop-on-fail loop (first-gate failure, last-gate failure, zero gates), the bind-mount pre-flight probe failing, docker build failing, .odin-version missing/empty/garbage, odin missing from PATH, TARGETARCH unset and uname -m returning something unexpected, the windows-cross rc!=0 vs rc==0-but-no-binary paths.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "edge",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

FILE-OUTPUT CONTRACT (mandatory): write ONLY the JSON array (no prose, no markdown fencing) to this exact absolute path using your write tool:
/Users/moses/code/_bmad-output/perkins/packet-plumber-local-ci-suite/r1/edge.json
Then stop. Do not print the findings into the chat; the file is the deliverable. An empty array [] written to the file is a valid, honest result.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
