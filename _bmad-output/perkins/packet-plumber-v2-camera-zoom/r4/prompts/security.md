You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. You are a REVIEW LENS: you never fix, never push, never merge — findings only.

--- INPUTS (absolute paths) ---
- DIFF: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r4/diff.patch
  (the canonical diff under review — 22 files, 2682 lines; the two docs/captures/*.png entries are binary one-liners; read it whole)
- WORKTREE (the checkout at exactly the reviewed sha af26d8a — every verification read happens here): /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-camera-zoom-r4
- PROJECT CONVENTIONS: /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-camera-zoom-r4/project-context.md
- SPEC / CONTEXT (review_mode = full):
  1. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r4/spec/job-briefing.md
  2. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r4/spec/perkins-briefing-r4.md

--- ROUND CONTEXT (round 4 — FIX AUDIT) ---
Round 4 of PR #89 (camera zoom/pan for an offline deterministic game — view-layer only). Round 3 found 2 blockers (pan clamped at live zoom; ungated debug-overlay toggle dead-zoning the release wheel) — head af26d8a claims all folded. Prior findings: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/consolidated.json (still-present prior items are carry-forwards, not new discoveries).

--- YOUR LENS (source tag: security) ---

OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

Honest scope note: this is an offline game view-layer (raylib + Odin) — much of the OWASP checklist does not apply; report ONLY what is genuinely present. Applicable surfaces in this diff:
- The settings file I/O (app/settings.odin — the v2 binary format, path handling, corruption fallbacks): deserialization of untrusted bytes (a corrupted/hand-crafted settings file — can it drive out-of-bounds reads, absurd values into the camera/a11y state?).
- The PP_DEBUG debug surface (the NOC overlay + its toggle): can any debug-gated behavior, state, or write leak into a RELEASE build (the B2 fold gates effect_overlay + falls the Noc_Scroll branch through — grep ALL overlay_on readers/writers and noc paths for release reachability)?
- Test hygiene: tests that write REAL user paths (r3 W2: a zeroed-App settings-adjust test writing the developer's real ~/.pp-settings.bin — verify whether still present in the worktree; a test mutating developer HOME state is a hygiene finding).
- CI workflow changes (.github/workflows/ci.yml): the added `odin test` step — any untrusted-input command construction (should be none; verify).
- The PR body / capture assets: any secrets, tokens, or personal paths embedded in the changed docs.

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path (create parent dirs if needed; write the file, do not print the JSON into chat):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r4/security.json

Each element must match this schema exactly:
{
  "source": "security",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<≤40 words>"
}

Output contract:
- The file contains ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing (likely here — do not stretch).
- Do not invent findings to fill a quota.
- After writing the file, STOP. Do not fix anything. Do not push. You are a reviewer.

ACCURACY MANDATE: every finding will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY. Open the file, read the lines, paste them verbatim in `evidence`. Hedging ("might", "could") means you have not verified — drop it. Accuracy > volume.
