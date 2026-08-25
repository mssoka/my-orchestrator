## 🤖 Perkins automated review — round 2 (cap lifted — loop until approved)
**Job:** packet-plumber-v2-7.2-audio-juice · **Reviewed sha:** 1b96bea · **Reviewers:** 7/7 completed
**Verification:** 16/18 findings confirmed against the code — 2 discarded as false-positive

### Fix audit (r1 → r2) — all 14 r1 findings verified FIXED
Re-derived from the code at `1b96bea`, not from the fix claims:

- **B1 (blocker) — M-mute chain ALIVE end-to-end:** `poll.odin` emits `Key_Press{.M}` → `mouse.odin` phase-1 collects `.M` (keys `[4]→[5]Key`, exact fit with the P/Space coalesce) and maps `case .M: append(out, Intent(Toggle_Mute{}))` — the prescribed shape → `types.odin` `Key.M` + `Toggle_Mute` in the union → `exec.odin` `case Toggle_Mute → on_mute` → `main.odin` wires `on_mute = effect_mute` → `au.toggle_mute` flips `Audio.muted` (+ StopSounds); `audio_flush` drops staged plays while muted; captions keep setting while muted (HUD shows the caption, else the "audio muted - press M" pill). M press actually mutes.
- **W1 caption clobber** — FIXED: `caption_crisis_live` guard; an unexpired crisis caption is never clobbered by an arrival (unit-tested: same-batch win, in-dwell protection, post-expiry handoff).
- **W-golden per-kind** — FIXED: `crisis_draws`/`arrival_draws` counters + harness asserts both ≥ 1 for `audio.dem` (strictly stronger than the old total-draws guard).
- **W-throttle unasserted** — FIXED: new `demos/audio_throttle.dem` (wide path, express-lane burst) + harness asserts `suppressed ≥ 1`; unit test pins the 4-event burst → 2 plays / 2 suppressed.
- **W-captions/asset coverage** — FIXED: 7 new `odin test app/audio` unit tests (draws, throttle, caption priority/expiry/reset, `wav_pack` bytes, synth forms, variant bounds) — **Perkins ran them at this sha: 7/7 PASS**; failed-decode `UnloadSound` hygiene added.
- **W-README contradiction** — FIXED: `assets/audio/README.md` carries the FINAL ruling (SFX = ElevenLabs; music = Suno Premier, user-owned; ElevenLabs Music set aside) + the three terms notes; matches the PR body.
- **All 6 notes folded:** `pending.*_plays` → u16 · dead `SYNTH_RAMP_S` removed · `audio.dem` header corrected — **probe-verified TRUE** (stats-stream run: first arrival tick 16 = era-3 director streaming demand, before the first explicit spawn at tick 41; final score 227 matches the r1 probe) · flush cycles variants for multi-play batches · Game_Over frozen-caption verified **unreachable by construction** (`draw_hud`'s Game_Over branch returns before `draw_audio_caption`) · restart-freshness covered by the reset unit test.

**Rebase check:** clean. The PR diff is r1-fix + folds ONLY; #59's files (`controller.odin`, `popover.odin`, `parity.odin`, CI) are untouched by this PR; gate 9 (input parity — #59's surface) green.

**Mechanical checks at the reviewed sha:** `tools/ci-local.sh --mac` **9/9 PASS** (31 demos incl. both audio goldens with the new guards, drift legs, input parity) · `odin test app/audio` **7/7 PASS** · zero non-audio demo/golden paths in the diff (the 29 pre-existing demos unshifted). (GitHub Actions remains org-billing-blocked — not a signal; the local suite is ground truth.)

### Blockers (0)
_None._

### Warnings (3)
1. **The 7 new `app/audio` unit tests run in NO gate** [codebase, tests] — `tools/ci-local.sh` + `.github/workflows/ci.yml` execute only `odin test core`; nothing runs or compiles `audio_test.odin` in a gate, so caption-priority/`wav_pack`/throttle-arithmetic regressions fail no gate. The r1 W2/W5 fold deliverable is real (7/7 PASS, verified) but ornamental in automation. *Fix:* add `odin test app/audio` to gate 2 in both files (the mirror rule); check the container leg's raylib link story. *(Demoted from the tests lens's blocker per the r1 re-triage precedent: the ODN-15 determinism spine is 100% gate-pinned incl. the new per-kind guards — this is durability, not correctness at this sha.)*
2. **The r1-B1 M-mute chain has zero automated coverage** [tests] — no scripted `.M` anywhere in the harness or unit tests. The fix is verified alive today, but the exact bug class that was r1's blocker has no regression pin. *Fix:* a parity leg scripting `Key_Press{.M}` asserting `Toggle_Mute` fires, and/or a zero-`Audio` mute toggle unit test.
3. **Advisory test gate: CONCERNS** [tests] — P0 (ODN-15) 100% + gate-pinned; P1 pins exist but are partially ungated (warnings 1–2). Wiring the tests + one `.M` pin raises the gate to PASS.

### Notes (9)
- **Throttle cold-start** [blind, edge]: `arrival_last_tick=0` doubles as "clicked at tick 0" — a first arrival at tick 0/1 would be suppressed with no prior click (and count in the W4 `suppressed` metric). Unreachable in practice (empty-map start; demos spawn ≥ tick 2); a sentinel (`max(u64)` / `has_clicked`) makes it clean.
- **Suno stragglers** [acceptance, codebase]: five code comments still say "drop Suno files" for the SFX slots (`audio.odin:6,19,52,254`, `main.odin:204`) — the FINAL ruling (SFX = ElevenLabs) is in the README/PR body; the module's own comments missed the fold.
- **Stale vacuous-guard docs** [blind, codebase]: `run.odin:308` still describes a "`draws>0` check" and `audio.odin:95` calls `draws` "the harness's vacuous-guard" — the harness now guards per-kind and never reads `draws`.
- **PR body §2 stale** [acceptance]: the acceptance paragraph still says "`draws > 0` vacuous-guard", one golden — superseded by the body's own W3/W4 rework bullets (per-kind + `audio_throttle.dem`).
- **Name-keyed harness consumer** [architecture]: `audio_consumer_on := name == "audio" || name == "audio_throttle"` — a future third audio golden added without a `run.odin` edit runs with no consumer AND no guards. A demo directive (`audio on`) makes goldens self-describing.
- **`Caption.text` buf-view comment** [blind]: arrival captions assign a string literal, not a `buf` view — harmless (static), but the stated invariant is false for the arrival path.
- **`audio_destroy` guard asymmetry** [blind]: closes the device even when init failed — **verified harmless** against the vendored raylib 6.0 source (`CloseAudioDevice` is `isReady`-guarded, no-ops).
- **Asset error paths manual-only** [tests]: corrupt-file `UnloadSound` + device-absent fallback have no automated coverage — the r1-accepted documented-manual route; PR body carries the smoke evidence.
- **Flush variant-cycle untested** [tests]: the `(variant+k)%N` cycle math is pure but unpinned (verified safe: bounded, non-negative, in-bounds).

### Reviewer agreement
- **Ungated unit tests** (codebase + tests) — the top follow-up.
- **Throttle cold-start** (blind + edge), **Suno comment stragglers** (acceptance + codebase), **stale guard docs** (blind + codebase).

**Verdict:** READY TO MERGE

The r1 blocker chain is alive, every pin bites, all folds verified, the rebase is clean, and the suite is green at the reviewed sha. The 3 warnings + 9 notes are follow-up polish (gate-wiring + one `.M` pin + doc sweeps) — non-blocking; fold them into 7.3 or a hygiene pass. Approving.
