## 🤖 Perkins automated review — round 1 (cap lifted — loop until approved)

**Job:** packet-plumber-v2-7.2-audio-juice · **Reviewed sha:** 84b46cc · **Reviewers:** 7/7 completed
**Verification:** 21/21 findings confirmed against the code — 0 discarded as false-positive

**Mechanical checks (Perkins, in the reviewed worktree):**
- `tools/ci-local.sh --mac`: **9/9 gates PASS** (native leg; the audio golden + replay gate green).
- **Audio probe** (scratch copy, instrumented counters): `draws=228, crisis_plays=1, arrival_plays=227` — the determinism golden genuinely exercises BOTH alert kinds, and the replay gate (consumer absent in `replay_hashes`) is real. ODN-15 neutrality: **proven, non-vacuous.** The `draws==0` negative-control guard exists and bites by construction.
- **Zero golden shifts**: the diff touches only NEW files (`goldens/audio.t1`, `goldens/audio.log.bin`, `demos/audio.dem`) — no pre-existing golden/demo/data modified. 29→30 demos.
- Consumer purity confirmed structurally: `consumer_consume(events, catalogs)` has no path to `Run_State`; `rng_range` upper bound verified inclusive; `fmt.bprintf`+`cstring` conversions safe via Odin ZII.

### Blockers (1)

**B1 — M-key mute chain broken: `Key_Press{.M}` is never translated to `Intent(Toggle_Mute)` — the entire mute path is dead** `[blind, edge, acceptance, architecture, codebase, tests]`
`app/input/mouse.odin:79-90,116-123,314-341` (phase-1 collect, phase-1 switch, phase-2 switch) · `app/input/poll.odin:60`
poll.odin emits the device event, types.odin declares `Key.M` + `Toggle_Mute`, exec.odin handles it via `on_mute` → `effect_mute` — but NEITHER mouse.odin phase (nor controller/touch) ever maps `Key.M` to the intent. Pressing M does nothing; acceptance "M mutes through the intent layer" fails at runtime. Verified three ways (no `case .M` exists anywhere in `app/input/`).
**Fix:** add the mapping in mouse.odin phase-1 (collect `.M` like `.T`, then `case .M: append(out, Intent(Toggle_Mute{}))`). Lane note: mouse.odin is untouched by BOTH #60 and #59 — the fix is collision-free. The #59 overlap is on `types/exec/poll.odin`; keep this PR's hunks there minimal (they currently are).

### Warnings (6)

1. **Caption slot is last-writer-wins: coincident alerts clobber each other** `[blind, edge]` — `app/audio/audio.odin:167-180`. Same-tick crisis wins (flow emits arrivals before the crisis engine — verified), but on catch-up frames a later-tick arrival clobbers an earlier crisis caption before it renders one frame. "Every audio alert captioned" fails for any alert followed by another in the same batch. Fix: crisis-priority (skip arrival `set_caption` while a crisis caption is in dwell) or a small queue.
2. **PR body claims ElevenLabs terms notes are "carried in `assets/audio/README.md`" — the README carries none and names only Suno** `[codebase]` — `assets/audio/README.md:34`. The body relays same-day rulings (ElevenLabs SFX; perpetual rights; sublicensing opt-out toggle; Studio Games tier) and says the README carries them — it doesn't. Update the README (or correct the body): one supplier story, written where the contract lives.
3. **The golden can't prove the crisis→sting draw per-kind** `[tests]` — the vacuous-guard counts TOTAL draws. Today's run is proven real (probe above), but if the surge recipe rots, arrival draws alone keep it green. Fix: assert per-kind minimums (crisis ≥1, arrival ≥1) for the audio demo.
4. **Arrival throttle exercised but never asserted** `[tests]` — a regression to click-per-arrival (busy-tick buzz) stays green. Fix: dense-arrival assertion (`plays < arrivals`) or a scripted-tick unit test on the pure consumer.
5. **Captions have zero automated coverage** `[tests]` — text, 40-tick dwell, expiry, live-while-muted, mute pill (demoted from the lens's blocker: HUD text has no golden precedent — rigor gap, not a merge blocker). The pure consumer half is device-free and unit-testable.
6. **Asset fallback/synth path untested** `[tests]` — corrupt-file fall-through (also: the failed `Sound` isn't unloaded before the placeholder path), `wav_pack` header math, device-off fallback. Fix: unit-test the packer; document the rest as manually verified. **Advisory test gate: CONCERNS** (P0 determinism 100% + probe-proven; P1 gaps as above).

### Notes (7)

- u8 `pending.*_plays` accumulates unflushed in the harness mirror — wraps past 255 (today peaks at 227; never read there — latent only). `[blind]`
- `SYNTH_RAMP_S` declared but unreferenced (ramp uses hardcoded `SYNTH_RAMP_SAMPLES`). `[blind]`
- `audio.dem` header claims arrivals "from tick ~16 on"; first spawn is 2000ms (tick 40), fixture off. `[blind]`
- Multiple crisis events in one batch collapse to N plays of the LAST-drawn variant. `[edge, architecture]`
- Caption never expires on the Game_Over screen (frozen `app.tick`; `draw_audio_caption` runs in every mode). `[edge]`
- Per-run freshness (`audio_reset_run` + `audio_mark=0`) has no restart coverage. `[tests]`
- Throttled-arrival semantics (silent AND uncaptioned) confirmed BY DESIGN — kept for the record, no action.

### Reviewer agreement

The blocker carries **6/7 lenses** (all but security, which correctly returned empty); the caption-contention warning carries 2. The ODN-15 hard-blocker class is **clean** — determinism neutrality is proven by a real, non-vacuous gate; asset contract is sound; the existing suite is unshifted (9/9 native). This round's changes are about the mute wiring, the caption contention, the README contradiction, and test rigor — NOT the determinism spine.

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha._
