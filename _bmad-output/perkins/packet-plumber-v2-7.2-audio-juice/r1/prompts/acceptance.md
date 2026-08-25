You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any file in the repository.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.2-audio-juice-r1/project-context.md (project conventions). Key invariants you must honor in judgment: `core/` is pure — imports only whitelisted `core:*` packages, never `vendor:*`, never `core:os`, never `core:time` (ODN-1); the sim steps only via `core.step`; integer-only sim math, floats only in the view (ODN-10); never iterate a map in core — arrays/slices only, maps lookup-only (ODN-9/10); sim RNG is owned by Run_State (ODN-9) and cosmetic/presentation randomness comes ONLY from the app-owned second stream (ODN-15); arena discipline (ODN-18); events, not callbacks (ODN-14 — the per-tick Event buffer on Run_State; the app reads a mark-based NEW slice but NEVER drains the buffer — the 4.2 tripwire); determinism is the project spine.

--- DIFF ---
Read the canonical diff FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.2-audio-juice/r1/diff.patch (2186 lines, unified format, PR #60 of solarity-services/Packet-Plumber, base branch v2, story 7.2 "audio juice"). These exact bytes are the review target — never re-fetch or regenerate the diff. Note: ~1400 of those lines are the new goldens/audio.t1 hash manifest (a per-tick FNV-1a list — skim its header, do not read every hash), and goldens/audio.log.bin is binary (a blessed action log — do not attempt to parse it; its gate is code-reviewed, not byte-reviewed).

--- WORKTREE (your verification source) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.2-audio-juice-r1 — a checkout at exactly the reviewed sha (84b46cc4fbd54187a135892dfa00a0a8ba81be46). Every verification read happens here. Trust this checkout, not origin/v2.

--- SPEC / CONTEXT ---
- Job briefing (the spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.2-audio-juice/r1/spec/job-briefing.md — note especially the Mission's 5 numbered hard requirements, the 4 numbered Acceptance criteria, and the Scope guard.
- Story 7.2 card: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.2-audio-juice/r1/spec/story-7.2-card.md (Given/When/Then + edge-case contracts).
- Sprint plan slice 7: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.2-audio-juice/r1/spec/sprint-plan-slice7.md (7.2's exit-criteria row: "SFX variant cosmetic-only [ODN-15]").
- PR body (claims to VERIFY, not facts): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.2-audio-juice/r1/spec/pr-body.md.

--- LENS-GUARDS (dispatching orchestrator's rulings — prevents false positives; honor them) ---
- [THE ONE HARD BLOCKER CLASS — ODN-15 determinism neutrality] Audio events must NEVER perturb the sim. Verify: (a) the consumer (`consumer_consume`) reaches ONLY the app-owned cosmetic rng — its signature (events + catalogs, no Run_State) means the sim rng is untouchable BY CONSTRUCTION; (b) the T1 determinism golden is REAL — the harness interleaves the real consumer between steps in the live path, and the replay gate (`verify_replay`/`replay_hashes`) re-sims the blessed log WITHOUT the consumer and must match byte-identically; a vacuous golden (consumer never draws, or a gate that cannot fail) is blocker-class — the claimed negative control is the `draws == 0` guard added in harness/run.odin; (c) no wall-clock, no randomness in the sim path; the app's event slice is mark-based (`events[audio_mark:]`, watermark advanced after consume) and 4.2-tripwire-safe (the app never drains state.events — a surge tick cannot drop or duplicate audio events).
- Asset contract: procedural placeholder tones (PCM16 WAV synthesized in memory) behind the documented Suno drop-in (assets/audio/README.md); the variant count is FIXED (3+3) so the golden stays asset-independent.
- Throttle policy (by design): at most 1 arrival click per 2 ticks, keyed on the EVENT's tick (`e.tick`) so catch-up frames stay throttled; suppressed arrivals are silent AND uncaptioned BY DESIGN (no alert happened). Do not flag the design; flag deviations from it.
- Captions: every PLAYED audio alert is captioned on-screen; M mutes through the 5.4 intent layer (Toggle_Mute intent + on_mute effect); captions stay live while muted.
- Existing suite unshifted: the PR claims zero golden shifts for the 29 pre-existing demos (the diff must touch ONLY new golden files) and 9/9 ci-local gates. The orchestrator verifies the suite mechanically — you verify CODE claims.
- LANE-AWARENESS FLAG (coordination, not a defect class): this PR touches app/input/{types,input,exec,poll}.odin — the SAME files the sibling 5.5 PR #59 (demolish input) touches. Review those hunks for scope creep / design collisions: the claimed touch is the M-mute key + Toggle_Mute intent + on_mute effect ONLY. Anything beyond that in those files = flag it. The touch must be minimal and idiomatic to the 5.4 intent layer — and COMPLETE: trace the full path device-event -> intent -> effect (a link missing anywhere in that chain is a real finding, not lane noise).
- What NOT to re-litigate (settled): the 5.4 intent-layer architecture itself (4 approved rounds); the core sim (no audio in core by construction — verify, don't re-architect); the 4.2 surge/crisis event semantics; ODN-15's established determinism spine; the 2.3 demolish core. Findings re-opening settled design are discarded.
- Base = v2 (post-#57 head). Fresh PR, round 1.

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

The binding contract, with the exact phrases to audit against (from the job briefing + story card + the orchestrator's guards):
1. "crisis fires → sting; arrival → click; variant from cosmetic rng only; captions shown" — trace EACH clause to code that actually executes end-to-end (declaration is not execution; a declared-but-unreachable path is a MISSING implementation finding).
2. "M mutes through the intent layer; captions live while muted" (orchestrator guard) — trace the FULL chain for the M key: device poll -> device event -> intent translation -> apply_intent -> on_mute effect -> toggle_mute. Every link must exist.
3. "rate-limited so a busy tick doesn't become a buzz — pick a sane, documented throttle" — 1 click / 2 ticks keyed on e.tick, documented.
4. "procedurally generated placeholder tones ... behind a clean asset-drop contract: documented path + naming + format ... loaded from disk when present, placeholder fallback when not" + "the golden must stay asset-independent (variant count fixed)".
5. "the T1 golden asserts audio events don't perturb the sim hash (same log → byte-identical replay, audio on or off)" + the vacuous-guard negative control.
6. "Existing suite unshifted" — the diff must not modify any pre-existing golden/demo/data files; "Default audio ON for the runnable game, OFF (or mock-silent) in the harness — goldens never capture audio state".
7. Acceptance #3: "PR body carries: the module shape (home, lifecycle, event wiring), the cosmetic-rng proof + citation [ODN-15], the throttle policy, the asset-drop contract, the caption surface used" — audit spec/pr-body.md for each item.
8. Acceptance #4: "Story card status line updated in the same PR" — verify the stories-v2.md hunk.
9. Scope guard: "2 stings, no soundtrack, no ambience, no mixer UI, no settings page ... No core changes, no sim-rng touches, no GDD/canon changes ... Do NOT generate or fetch real audio assets". Flag anything beyond it. Your `source` value is "acceptance".

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. determinism, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

FILE-OUTPUT CONTRACT (headless mode): using your file-write tool, write ONLY your JSON array (valid JSON, no prose, no markdown fencing, no preamble) to exactly this absolute path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.2-audio-juice/r1/acceptance.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens acceptance complete — N findings written".
