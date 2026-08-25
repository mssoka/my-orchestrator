You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any file in the repository.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.2-audio-juice-r2/project-context.md (project conventions). Key invariants you must honor in judgment: `core/` is pure — imports only whitelisted `core:*` packages, never `vendor:*`, never `core:os`, never `core:time` (ODN-1); the sim steps only via `core.step`; integer-only sim math, floats only in the view (ODN-10); never iterate a map in core — arrays/slices only, maps lookup-only (ODN-9/10); sim RNG is owned by Run_State (ODN-9) and cosmetic/presentation randomness comes ONLY from the app-owned second stream (ODN-15); arena discipline (ODN-18); events, not callbacks (ODN-14 — the per-tick Event buffer on Run_State; the app reads a mark-based NEW slice but NEVER drains the buffer — the 4.2 tripwire); determinism is the project spine.

--- DIFF ---
Read the canonical diff FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.2-audio-juice/r2/diff.patch (2587 lines, unified format, PR #60 of solarity-services/Packet-Plumber, base branch v2 @ 388e316 (post-#59 merge), story 7.2 "audio juice" — ROUND 2: this is the fix-audit delta after a round-1 CHANGES_REQUESTED review). These exact bytes are the review target — never re-fetch or regenerate the diff. Note: ~1400 of those lines are the new goldens/audio.t1 hash manifest (a per-tick FNV-1a list — skim its header, do not read every hash), ~87 lines are goldens/audio_throttle.t1 (same shape), and goldens/*.log.bin are binary (blessed action logs — do not attempt to parse them; their gate is code-reviewed, not byte-reviewed).

--- WORKTREE (your verification source) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.2-audio-juice-r2 — a checkout at exactly the reviewed sha (1b96bea688e44db021eca8a98b9fc9cded27daff). Every verification read happens here. Trust this checkout, not origin/v2.

--- SPEC / CONTEXT ---
- Job briefing (the spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.2-audio-juice/r2/spec/job-briefing.md — note especially the Mission's 5 numbered hard requirements, the 4 numbered Acceptance criteria, and the Scope guard.
- Story 7.2 card: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.2-audio-juice/r2/spec/story-7.2-card.md (Given/When/Then + edge-case contracts).
- Perkins r2 fix-audit briefing: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.2-audio-juice/r2/spec/perkins-briefing-r2.md (the r1 findings + the claimed fixes — YOUR job is the fresh-diff review for NEW defects and INCOMPLETE/botched fixes, not re-deriving the fix audit; the orchestrator owns the formal fix-audit classification).
- PR body (claims to VERIFY, not facts): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.2-audio-juice/r2/spec/pr-body.md.

--- ROUND CONTEXT (r2 — what this diff IS) ---
Round 1 (sha 84b46cc) was CHANGES_REQUESTED: 1 blocker + 6 warnings + 6 notes. This r2 diff is the SAME PR force-pushed: the r1 feature PLUS the r1 fixes, rebased onto v2 @ 388e316 (which merged PR #59 — the 5.5 demolish pad-X controller leg + popover refactor). The r1→r2 fix claims (each claims COMPLETE — verify the fix code is sound, and hunt NEW defects the fixes introduce):
- B1 (the r1 blocker): the M-key mute chain was dead — poll emitted Key_Press{.M} but no mapper collected it. Claimed fix: app/input/mouse.odin phase-1 collects .M (keys array [4]->[5]) and maps `case .M: append(out, Intent(Toggle_Mute{}))`; exec.odin handles Toggle_Mute -> on_mute; app/main.odin wires on_mute = effect_mute -> au.toggle_mute.
- W1: coincident alerts clobbered the single caption slot. Claimed fix: crisis-priority — an arrival skips set_caption while an unexpired crisis caption is live (caption_crisis_live).
- W2/W5 (tests): zero caption coverage + asset-fallback untested. Claimed fix: 7 new unit tests in app/audio/audio_test.odin (draws, throttle, caption priority/expiry/reset, wav_pack header bytes, synth forms, variant bounds).
- W3: the vacuous-guard counted TOTAL draws only. Claimed fix: per-kind counters (crisis_draws/arrival_draws) + harness asserts >= 1 each for audio.dem.
- W4: throttle never asserted. Claimed fix: new demos/audio_throttle.dem (dense adjacent-tick arrivals) + harness asserts suppressed >= 1.
- W6 (docs): PR body vs assets/audio/README.md supplier contradiction. Claimed fix: README now carries the FINAL ruling (SFX = ElevenLabs; music = Suno Premier, user-owned; ElevenLabs Music set aside) + terms notes.
- Notes: pending.*_plays u8->u16; dead SYNTH_RAMP_S removed; audio.dem header corrected (director demand, ~tick-16 arrivals); audio_flush CYCLES variants for multi-play batches; the Game_Over frozen-caption note documented harmless (the draw_hud Game_Over branch returns before draw_audio_caption); restart-freshness coverage via the reset unit test.

--- LENS-GUARDS (dispatching orchestrator's rulings — prevents false positives; honor them) ---
- [THE ONE HARD BLOCKER CLASS — ODN-15 determinism neutrality] Audio events must NEVER perturb the sim. The r1 probe proved the shape non-vacuous (228 draws, 1 crisis + 227 arrivals, replay gate byte-identical, consumer structurally pure). Verify the r2 changes keep it: consumer_consume still has NO sim access (events + catalogs only); the harness interleaves the consumer BEFORE the hash; the replay gate re-sims WITHOUT the consumer; the per-kind vacuous-guards can actually fail (they append to the same fails list the run honors).
- Asset contract (FINAL user ruling 2026-08-17 — settled, do NOT re-litigate): SFX = ElevenLabs; music = Suno Premier (user-owned perpetual commercial rights incl. video games); ElevenLabs Music set aside. Placeholder tones synthesized; variant count FIXED (3+3) so the golden is asset-independent.
- Throttle policy (by design): at most 1 arrival click per 2 ticks keyed on e.tick; suppressed arrivals are silent AND uncaptioned BY DESIGN. Do not flag the design; flag deviations.
- Captions: every PLAYED audio alert is captioned; M mutes through the 5.4 intent layer; captions stay live while muted; the muted state shows an "audio muted - press M" pill when no caption is live.
- Existing suite unshifted: 29 pre-existing demos; the diff must touch ONLY new golden/demo files (audio*). The orchestrator mechanically verified 9/9 ci-local native gates PASS at the reviewed sha + odin test app/audio 7/7 PASS — you verify CODE claims.
- INPUT-LAYER TOUCH (expected, prescribed): the app/input hunks are Perkins' own prescribed r1-B1 fix shape (collect .M like .T; map to Toggle_Mute; exec case; on_mute wiring). #59 is MERGED into the base — no sibling lane. Flag only: anything BEYOND the M-chain in app/input, or a missing link in poll -> collect -> intent -> exec -> effect -> audio.muted.
- REBASE-AWARENESS: the PR diff must be r1-fix + folds ONLY, cleanly rebased. #59's intent-layer additions (pad-X controller leg, popover refactor, parity legs) must be present in the tree and untouched by this PR — files like app/input/controller.odin, app/render/popover.odin, harness/parity.odin are NOT in this diff; if you find this PR reverting or double-applying #59 content, that is a finding.
- What NOT to re-litigate (settled): the 5.4 intent-layer architecture; the core sim; the 4.2 surge/crisis event semantics; ODN-15's spine; the #59 demolish surface (approved + merged); the asset-contract source rulings; r1's discarded false-positives (bprintf cstring safety via ZII, rng_range inclusive-hi bounds, the u8-wrap now-moot widening). Findings re-opening settled design are discarded.

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

Context for this codebase (derive your own classes too — and NOTE: several of these were r1 findings with CLAIMED fixes; trace whether the fix actually closes the path or leaves a residual): throttle first-click boundary (`arrival_last_tick` starts 0 — arrivals at tick 0/1?); catch-up frames (multi-tick slices in ONE consume — ordering, e.tick-keyed throttle); watermark desync (audio_mark vs len(state.events) across pause, win/loss, retry — who re-makes the buffer, who resets the mark); the W1 crisis-priority guard (an arrival arriving BEFORE its crisis in the same tick-batch — core emits arrivals before crises; a crisis at tick T then an arrival at tick T+40 exactly: `tick <= until_tick` boundary); the flush variant-cycle (N staged plays cycle (last+k)%N — with u16 plays and i32 variant arithmetic, any overflow/modulo-negative path?); caption buffer [96]u8 vs a long crisis display_name (bprintf truncation); `e.archetype` bounds in crisis_caption (type? negative? stale after catalog reload?); audio device absent (silent fallback — captions still update? flush safe?); corrupt/zero-frame asset (LoadSound path — now UnloadSound's the failure; double-free? leak?); `fmt.bprintf` + `cstring(raw_data(path))` termination and the [64]u8 path_buf; rng_range bounds (inclusive hi — verify in core/rng.odin); synth math (ramp at buffer ends, `int(dur_s * RATE)` truncation, wav_pack u32 casts, `idx % VARIANTS` with negative idx); mute pressed between consume and flush (staged plays dropped — intended?); harness per-TICK vs app per-FRAME consume granularity (same draw sequence?); the audio_throttle.dem recipe (wide cap 40 -> 1 tick per edge claim; 500/550/600 ms -> ticks 11/12/13? does it REALLY produce adjacent-tick arrivals — check the golden it blest: ticks=80 for a 4000ms run); the unit tests themselves (do the expected values match the implementation? e.g. throttle admits 100 + 102 but the 4-event burst in the test — what does event tick 100 twice do to `arrival_last_tick`?). Your `source` value is "edge".

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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.2-audio-juice/r2/edge.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens edge complete — N findings written".
