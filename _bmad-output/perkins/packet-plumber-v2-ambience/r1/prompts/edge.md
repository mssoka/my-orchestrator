You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

Your working directory IS the reviewed worktree — a detached checkout at exactly the reviewed sha. Every verification read happens there. NEVER edit files, never run mutating git commands, never fetch from the network, never re-generate the diff.

--- PROJECT CONVENTIONS ---
Read project-context.md at the repo root (your cwd) — that is the project conventions doc. There is no CLAUDE.md.

--- DIFF ---
The canonical diff is saved at:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-ambience/r1/diff.patch
Read that file (the whole thing — ~2100 lines, page through all of it). Review EXACTLY those bytes. Never re-fetch or regenerate the diff (no `git diff`, no `gh pr diff`).

--- SPEC / CONTEXT ---
The spec (the original job briefing — it IS the spec; there is no GitHub issue) is at:
/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-ambience.md
Read it in full before judging anything.

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

--- ROUND FOCUS (reviewing orchestrator's hard blocker bar — verify, don't assume) ---
(a) T1/T2/replay must be byte-identical — ZERO golden diffs (if any golden moved, that's a bug).
(b) No audio-device failure may crash a headless/CI run (the harness must survive 'no audio device' — the #81 event-sound precedent).
(c) The bed must layer BESIDE the #81 event system (append-only event tags stay the SFX path — not rebuilt).
(d) The committed asset must be the COMPRESSED form (OGG ~913KB); the 35MB vault WAV must never be committed; the transform must be reproducible + sha256-pinned.
Do NOT re-litigate: the Suno bed choice itself, the seamless-loop window + crossfade approach, and placement decisions (starts with run, Pause soft-lowers, Mute pauses in place) are user-ruled/minion-picked and documented. The stage-3 intensity-layers plan is OUT of scope.
Edge paths of particular interest this round: the no-audio-device / InitAudioDevice-failure path; the ducking envelope boundary math (0.30s duck to 0.12 + 0.60s ramp, relative + capped — what happens at volume extremes, repeated triggers, pause/mute mid-duck); loop wrap handling; mute/pause interactions.

--- OUTPUT ---
Produce ONE valid JSON array. Each element must match this schema exactly:
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

Output contract: the JSON array only. No prose, no fencing, no preamble. Empty array `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

--- FILE-OUTPUT CONTRACT (this is how you deliver) ---
Write ONLY the JSON array to this exact absolute path (create parent dirs if needed):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-ambience/r1/edge.json
No prose around the JSON in the file. Then STOP. In the chat, reply with one short line only: "wrote edge.json (<n> findings)".
