## 🤖 Perkins automated review — round 1
**Job:** packet-plumber-v2-sound-immediacy · **Reviewed sha:** 97f0e92 · **Reviewers:** 6/7 completed
**Verification:** 21/21 findings confirmed against the code — 0 discarded as false-positive

Lens disclosure: the acceptance lens failed twice on provider rate-limits (429) and is the one degraded layer; the spec-AC surface was covered by direct guard verification instead: **event→sound map extension confirmed (all four kinds fire across `audio.dem` + `audio_spawn.dem`), immediacy holds by construction (per-frame `events[audio_mark:]` drain = ≤1 frame ≈ 17 ms), and `tools/ci-local.sh --mac` is 10/10 green at the reviewed sha.** Guard checks the briefing pinned: change confined to the audio consumer + two append-only zero-payload tags ✓ (no LOG_VERSION bump, no packet/routing/visual changes — the debug-overlay tail is `PP_DEBUG`-gated); live fast-path and replay emit the same zero-payload event at the same apply tick ✓ (live passes `{}` to step, so each path has exactly one emitter); re-bless purity ✓ (44 `.t1` re-blesses + new `audio_spawn` pair, zero T2 pixels, zero modified `.log.bin`, moved ticks = draw apply ticks / spawn ticks).

### Blockers (2)

**1. Live fast-path `PIPE_DRAWN` append ships unpinned — a revert passes every CI gate** — `app/input/exec.odin:318-324` [architecture, tests, codebase, blind]
The shipped game's wire click depends solely on this 3-line append. Parity nils `sim_events` on purpose, the goldens drive step's batch path, live passes `{}` to step (`main.odin:367`), and no test drives `commit_draw` — deleting the append (or the `main.odin` wiring) is CI-silent, killing the feature and the live-side witness of the ODN-14 byte-identity claim. This repo's own r5/r6 "wiring shipped unpinned" blocker class.
*Fix:* exec-level test (`settings_effect_wiring` precedent): `Input` with a wired `sim_events` scratch buffer, drive `commit_draw`, assert exactly one `Event{tick = inp.tick+1, tag = EVENT_TAG_PIPE_DRAWN}` on a valid draw and none on an invalid one.

**2. Advisory test gate: FAIL** — P0 0% (the live wire-click path, blocker 1), P1 ~75%, overall ~70%. Same root cause as blocker 1 plus the missing core negative legs (warning 6); landing those pins lifts the gate.

### Warnings (6)

1. **"ALL FOUR kinds" claim for `audio.dem` is false** [blind, architecture, codebase, tests] — `harness/run.odin:506-509`, `demos/audio.dem` header, `_pr_body.md`. `audio.dem` has no `growth on`, so `NODE_SPAWNED` cannot fire there; its guard (correctly) asserts crisis+arrival+wire only, with spawn living in `audio_spawn.dem`. The comments self-correct mid-sentence but the headline misleads — reword all three spots.
2. **Spawn placeholder is 0.66 s of sequential tones — not "layered over ~0.3 s" and outside the README's own 0.2–0.4 s slot envelope** [blind, edge, codebase] — `audio.odin:432-441`. `tone_append` is append-only (no offset/mix): 0.22+0.30+0.14 = 0.66 s arpeggio. Mix the layers into ~0.3 s or fix comment + README to match the shipped waveform.
3. **`SPAWN_TICK` is an octave above its documented labels** [blind] — `audio.odin:86` + README. `{1175, 1320, 1046}` = D6/E6/C6; "a fifth above the body"/README's D5-E5-C5 = 587/659/523. A Suno file built to the README spec lands an octave below the placeholder. Halve the constants or fix the labels.
4. **`toggle_mute` stops only crisis+arrival — wire/spawn ring past a mid-sound mute flip** [edge] — `audio.odin:308-315`. The diff added two playable families but not the two `StopSound` loops; a mid-chime flip leaves the 0.66 s spawn chime ringing, against the "flip immediate" comment. Add the wire/spawn stop loops.
5. **Fast-path append falls outside the app's per-tick hash window — app stats stream no longer replay-identical at draw ticks** [architecture] — `main.odin:352-385`. The app appends `PIPE_DRAWN` at input time (outside the `events_before` step window) while harness/replay hash it inside the apply tick — the "app stream is replay-identical" comment is now false at draw ticks. Diagnostics-only (no gate compares it); defer the append to the step boundary or amend the comment.
6. **Core emissions pinned only via T1 hashes — no core unit test names tags 15/16; negative legs unpinned** [tests] — `core/step.odin:79-88,116-123`. T1 bites but localizes nothing; no named assertions for "no event on rejected command" / "no spawn with growth off", against project-context's pin-at-lowest-layer rule.

### Notes (5)

1. Stale "draw at 100 ms" copy in `audio_spawn.dem`'s header + the `run.odin` guard message — the recipe's draws are at 2000/2500 ms (the 1000 ms entry is a router place).
2. `load_variant` doc comment duplicated — orphaned copy above the `Sound_Kind` enum (`audio.odin:331-333`).
3. `kind_volume`'s trailing unreachable return masks a future non-exhaustive switch (`audio.odin:352`).
4. Immediacy AC (~50 ms) is by-construction only — no pin of the step→drain→flush ordering.
5. Wire/spawn flush loops join the untested device-gated surface; `audio_test.odin`'s header cites an "app smoke check" that exists in no CI gate (pre-existing 7.2 text).

### Reviewer agreement
- Live fast-path append unpinned — 4 lenses (architecture, tests, codebase, blind)
- "ALL FOUR kinds" claim false for audio.dem — 4 lenses (blind, architecture, codebase, tests)
- Spawn placeholder 0.66 s sequential vs documented ~0.3 s — 3 lenses (blind, edge, codebase)

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
