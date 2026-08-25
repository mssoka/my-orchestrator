# r2 FIX AUDIT — Perkins' own verification against the worktree @ 1b96bea
# Every r1 finding re-read against the current code. Status: fixed | still-present

## B1 (blocker, 6-lens) — M-key mute chain dead → FIXED
Chain verified end-to-end at 1b96bea:
- app/input/poll.odin:61 `if rl.IsKeyPressed(.M) { append(&inp.events, Device_Event(Key_Press{key = .M})) }`
- app/input/mouse.odin phase-1 collect: `case .M: if keys_n < len(keys) { keys[keys_n] = .M; keys_n += 1 }` (keys array widened [4]→[5]Key — P/Space coalesce to one slot, so max = P,D,T,M,Esc = 5: exact fit, overflow-guarded)
- app/input/mouse.odin phase-1 emit: `case .M: append(out, Intent(Toggle_Mute{}))` — Perkins' prescribed shape (collect like .T)
- app/input/types.odin: `M` in Key enum; `Toggle_Mute :: struct {}`; added to Intent union
- app/input/exec.odin: `case Toggle_Mute: if inp.on_mute != nil { inp.on_mute(inp.user, inp) }`
- app/input/input.odin: `on_mute` field on Input
- app/main.odin:269 `app.input.on_mute = effect_mute`; effect_mute → `au.toggle_mute(&app.audio)`
- app/audio/audio.odin toggle_mute: flips `a.muted`, StopSound on active sounds; audio_flush gates on muted (dropped, not queued); consumer_consume sets captions regardless of mute (captions stay live); draw shows caption else "audio muted - press M" pill
M press actually mutes; captions live while muted. CHAIN ALIVE.

## W1 (blind+edge) — caption clobber → FIXED
audio.odin arrival branch: `if !caption_crisis_live(&a.caption, e.tick) { set_caption(...) }`;
caption_crisis_live = live && crisis && tick <= until_tick. Core emits arrivals before crises
within a tick, so same-tick crisis still wins by write order; cross-tick catch-up clobber is
now blocked for the full 40-tick dwell. Unit test test_caption_crisis_priority pins
same-batch win, in-dwell protection, post-expiry handoff.

## r1-W (tests) captions zero coverage → FIXED
test_caption_crisis_priority + test_caption_expiry_and_reset: caption text, dwell live-at-end,
expiry at until_tick+1, reset_run clears caption + throttle. 7/7 PASS (odin test app/audio,
run by Perkins at the reviewed sha).

## r1-W (tests) per-kind draws → FIXED
Audio: crisis_draws + arrival_draws counters; harness/run.odin:465-471 asserts BOTH >= 1 for
audio.dem ("no crisis draw — the golden is vacuous" / "no arrival draw"). Old total-draws
guard replaced — per-kind is strictly stronger. Gate 4 green at sha (31 demos incl. audio).

## r1-W (tests) throttle unasserted → FIXED
demos/audio_throttle.dem (new): wide path + express-lane streaming, spawn burst 500/550/600ms;
harness/run.odin:472-476 asserts arrival_draws >= 1 AND suppressed != 0. Golden blessed
(ticks=80 for 4000ms — wait: 4000ms @ 50ms/tick = 80 ticks ✓). Gate 4 green.
Unit test test_consumer_arrival_throttle pins admission at ticks 100/102, suppression of
same-tick-dup + tick-101 (4 events → 2 plays, 2 suppressed).

## r1-W (tests) asset fallback untested → FIXED
test_wav_pack_header (RIFF/fmt/data fields + PCM16 LE sample bytes incl. negative + clamp);
test_synth_wav_forms (all 6 forms: header + non-silence); load_variant now UnloadSound's a
0-frame failed decode before the placeholder fallback (no orphaned stream buffer).

## r1-W (codebase) README/body supplier contradiction → FIXED
assets/audio/README.md "Sources (user ruling 2026-08-17, FINAL)": SFX = ElevenLabs;
music = Suno Premier (user-owned, perpetual commercial rights incl. video games);
ElevenLabs Music set aside (Studio Games exclusion); terms notes (a) perpetual commercial
rights, (b) SFX sublicensing Disable-toggle opt-out TODO, (c) Suno ownership. Matches the
(r2-updated) PR body — one supplier story in both places.

## r1-N u8 pending wrap → FIXED
Pending.crisis_plays/arrival_plays now u16 (comment cites the r1 note).

## r1-N SYNTH_RAMP_S dead → FIXED
Removed; only SYNTH_RAMP_SAMPLES (110) with the derivation comment remains.

## r1-N audio.dem header wrong (~tick 16) → FIXED
Header now attributes the early arrivals to the era-3 director's streaming demand and points
the dense-tick claim at audio_throttle.dem. PROBE-VERIFIED TRUE: harness --stats-out run of
audio.dem shows first delivered at tick 16, class 1 (streaming) — before the first explicit
spawn at 2000ms (tick 41). Final score 227 (matches r1's probe: 227 arrival plays).

## r1-N multi-crisis collapse → FIXED
audio_flush cycles variants per play: v = (last_variant + k) % VARIANTS for play k —
N staged plays stay distinguishable; the draw pattern is unchanged (one draw per trigger).

## r1-N Game_Over frozen caption → FIXED (moot — verified unreachable)
draw_hud's Game_Over branch RETURNS at main.odin:~909 (verified: `return` after the retry
hint); draw_audio_caption is called at ~1008, after the return → never draws on the
Game_Over screen. The new NOTE comment documents exactly this, accurately.

## r1-N restart freshness coverage → FIXED
test_caption_expiry_and_reset covers audio_reset_run (caption cleared, throttle reset →
first post-reset arrival plays immediately).

# REBASE CHECK (1b96bea on v2 @ 388e316, post-#59)
PR diff (base…head) touches ONLY: README.md, stories-v2.md, app/audio/* (2), app/input
{exec,input,mouse,poll,types} (M-chain only), app/main.odin, assets/audio/README.md,
demos/audio*.dem (2 new), goldens/audio* (4 new), harness/run.odin.
#59's files (app/input/controller.odin, app/render/popover.odin, harness/parity.odin,
.github/workflows/ci.yml, tools/ci-local.sh, decision-log.md) are NOT in the PR diff →
#59 present + untouched, zero rebase revert. Gate 9 (input parity — #59's surface) PASS.

# MECHANICAL CHECKS at the reviewed sha
- tools/ci-local.sh --mac: 9/9 PASS (EXIT=0) — incl. gate 4 (31 demos, audio + audio_throttle
  green with the new per-kind/suppressed guards), gate 5 drift-rejection legs incl.
  audio_throttle, gate 9 input parity.
- odin test app/audio: 7/7 PASS (850µs).
- harness run audio --stats-out: PASS; first arrival tick 16 (director demand) — header true.
- Golden hygiene: diff adds only NEW golden/demo files; the 29 pre-existing demos unshifted
  (zero non-audio demo/golden paths in the diff).

# NEW-FINDING CANDIDATES (Perkins' own, pending lens corroboration)
- CANDIDATE-A (warning): the 7 new app/audio unit tests run in NO gate — ci-local.sh GATES
  (9) and ci.yml steps contain only `odin test core`; tools/harness.sh builds but never
  odin-tests app/audio. The W5/W6 fold deliverable is ornamental in automation: a regression
  in caption priority / wav_pack / throttle arithmetic goes uncaught unless it perturbs a
  golden (goldens don't capture audio bytes or caption text). Fix: add `odin test app/audio`
  to ci.yml + ci-local.sh (the mirror rule — "never edit one without the other").
- CANDIDATE-B (note): harness/run.odin:308 comment still says "The draws>0 check (after the
  loop) is the vacuous-guard" — the actual checks are now the per-kind/suppressed guards
  (strictly stronger). Stale wording, meaning survives.
