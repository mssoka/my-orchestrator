You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read `/Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-node-clarity-r2/project-context.md` — that file's content IS the PROJECT CONVENTIONS block below.

--- DIFF ---
The diff under review is the exact bytes of `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-node-clarity/r2/diff.patch` — read that file; its content IS the DIFF block. (1257 lines, unified format. The long `goldens/**` section is binary PNG re-blesses — expected and documented in the spec/PR body; judge the text hunks on their merits.)

--- SPEC / CONTEXT ---
Read these two files; together their content IS the SPEC / CONTEXT block:
1. `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-node-clarity.md` — the job briefing (THE spec: task, hard rules, acceptance).
2. `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-node-clarity/r2/pr-body.md` — the PR body (the implementer's claims, the documented deviations D1–D7, and the "Rebase follow-up (r2)" section).

--- ROUND CONTEXT (r2 — rebase-delta fix-audit) ---
Round 1 reviewed this PR's substance (hue families, chips, tier markers) and APPROVED it (0 blockers, 5 warnings, 12 notes). Since then PR #77 (v2-network-pop) MERGED to the base first; this branch rebased onto the merged v2, resolved the palette `_comment` conflict keeping BOTH PRs' notes on one line, and re-blessed all 45 goldens under the COMBINED palette (commit 28be432, cause-documented in the PR body's "Rebase follow-up" section). The diff you review is the FULL PR vs the #77-merged base.

NOT re-litigatable (user rulings / r1 approvals — do not flag these as findings):
- The hue-family separation + chips + tier markers direction itself; the blur-gate ≥ 15° acceptance bar.
- The tuned anchors D2 (campus #A87250) and D3 (small_biz #6E9B74) — documented honest deviations, gate-driven.
- The 45-demo T2 re-bless being deliberate and cause-documented.
- The wash-at-draw-time approach (D1) and chips-skip-under-health-ring (D5).

The r2 review questions (frame your lens around them): (a) is the rebase onto the #77-merged base clean — both PRs' content kept, no token-key collisions (#77 owns router_led/pipe_*/packet_*/lane_*; this PR only ADDS *_family/router_tier_* keys)? (b) is the combined-palette re-bless sound — T1/spine byte-identity (the diff must contain ZERO .t1/.log.bin hunks) and the claimed blur-gate numbers unchanged (min pair 22.6°, sat band 0.289)? (c) any NEW issue introduced by the rebase or the second re-bless? Prior-round findings are carried forward separately by the orchestrator — your job is the current state, fresh eyes.

--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

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

Output contract:
- Write your JSON array to the file `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-node-clarity/r2/security.json` — that file must contain ONLY the JSON array (no prose, no markdown fencing, no preamble). Then reply with one short line confirming the write, and stop.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
