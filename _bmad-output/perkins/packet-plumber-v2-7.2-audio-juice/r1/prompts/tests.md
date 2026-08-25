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
Test coverage analysis via traceability. The project's testing rules (project-context.md): the golden harness is the verification foundation; T1 = state-hash goldens, T2 = pixel goldens; `odin test` for the pure core; invariants pinned as regression tests at the lowest layer.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify FULL / PARTIAL / NONE. Behaviour inventory for this diff: (1) crisis event -> sting variant draw; (2) arrival event -> throttled click variant draw; (3) ODN-15 determinism neutrality (consumer interleaved live vs no-consumer replay, byte-identical); (4) the vacuous-guard (draws==0 fails); (5) captions on played alerts; (6) M-mute toggle end-to-end; (7) asset drop-in + placeholder fallback; (8) per-run reset (throttle/caption/mark freshness); (9) the 29 pre-existing demos unshifted; (10) the audio demo recipe itself (does it actually produce BOTH event kinds — check what the golden can and cannot prove: the vacuous-guard counts TOTAL draws, not per-kind draws).

Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check: happy-path-only coverage where error handling is implied (device-absent fallback, corrupt asset file); new state transitions without boundary tests (mute on/off, restart freshness); a golden that cannot distinguish the behaviours it claims to pin (per-kind draw proof).

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS -> note, CONCERNS -> warning, FAIL -> blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds: PASS: P0 100%, P1 >=90%, overall >=80%; CONCERNS: P0 100%, P1 80-89%, overall >=80%; FAIL: P0 <100%, or P1 <80%, or overall <80%. Your `source` value is "tests".

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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.2-audio-juice/r1/tests.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens tests complete — N findings written".
