## 🤖 Perkins automated review — round 2
**Job:** packet-plumber-v2-sound-immediacy · **Reviewed sha:** 560d713 · **Reviewers:** 7/7 completed
**Verification:** 12/12 findings confirmed against the code — 0 discarded as false-positive

### Fix audit (r1 → 560d713) — 11 of 13 fixed, 2 carried

| r1 | Status | Notes |
|---|---|---|
| B1 unpinned live PIPE_DRAWN append | ✅ **fixed** | `app/input/exec_test.odin` drives the real `commit_draw`: valid draw → exactly one `Event{tick=inp.tick+1, tag=EVENT_TAG_PIPE_DRAWN}` + logged command at apply_tick + pipe applied; invalid (E26) → nothing; nil `sim_events` → no crash. Runs in ci-local gate 2. **Revert-control reproduced by the reviewer**: deleting the append fails the test. |
| B2 advisory gate FAIL | ✅ **fixed** | Gate flips to **PASS** — P0 100% (wire live exec-pinned pos/neg/nil; wire+spawn replay core-pinned pos/neg; guards bite), P1 ~94%, overall ~82%. ci-local 10/10 green at this sha. |
| W1 "ALL FOUR kinds" claim | ⚠️ **still present (partial)** | run.odin + audio.dem reworded correctly — but `_pr_body.md:17` still claims "audio.dem now proves ALL FOUR kinds fire". Corroborated by 2 lenses. |
| W2 0.66 s spawn arpeggio | ✅ fixed | `chime_append` mixes the 3 layers over one 0.32 s window (inside the README 0.2–0.4 s envelope); pinned by `test_spawn_chime_envelope_and_pitch`. |
| W3 SPAWN_TICK octave | ✅ fixed | {587, 659, 523} = D5/E5/C5 — a true fifth above the body, matching the README labels; 3:2 ratio pinned. |
| W4 toggle_mute scope | ✅ fixed | Muted branch now stops all four families. |
| W5 replay-identical claim | ⚠️ **still present — the doc fix is false** | The new main.odin comment + PR body claim "byte-identical slices, live vs replay". Mechanically false: `handle_input`'s append sits below the next step's `events_before` mark → excluded from every per-tick hash slice, while replay's command-loop emission lands inside its slice. The codebase's own `parity.odin` note states the correct mechanics. Corroborated by 2 lenses. |
| W6 core named legs | ✅ fixed | `core/sound_events_test.odin`: 4 named legs incl. both negatives (rejected draw → no event + `replay_error`; growth-off → no NODE_SPAWNED). |
| N1–N5 | ✅ fixed | Stale 100 ms copy → 2000/2500 ms; orphaned doc comment removed; `kind_volume` return documented (Odin switches are exhaustiveness-checked — the r1 premise didn't hold); immediacy ordering documented by-construction (reviewer sign-off given — AC accepted); audio_test header's false "app smoke check" claim replaced with the real coverage. |

**Byte-identity guard:** one emitter per path holds (live: `{}` to step + single fast-path append; replay: command-loop emission only; parity nils `sim_events`) — golden + replay gates green.

### Blockers (0)

None.

### Warnings (3)

1. **still present since round 1 — "ALL FOUR kinds" remains in the PR body** (`_pr_body.md:17`) [blind, acceptance] — audio.dem runs growth-off, so NODE_SPAWNED cannot fire there; reword to "audio.dem proves crisis+arrival+wire; audio_spawn.dem proves spawn+wire".
2. **still present since round 1 — the W5 "byte-identical slices" comment is mechanically false** (`app/main.odin:381-385`) [architecture, codebase] — the fast-path event is excluded from every per-tick hash slice in the live app (diagnostics-only divergence; no gate compares it); document the exclusion instead of asserting identity.
3. **Wire/spawn play+mute paths have zero automated coverage** (`app/audio/audio.odin:306-329`) [tests] — the flush `PlaySound` loops and `toggle_mute` `StopSound` loops are untested (guards pin draws only; device-gated half consistent with the 7.2 convention). P2.

### Notes (7)

- Wire placeholder comment says the thump sits "under" the tock — it's appended **after** it (`audio.odin:439-446`; 105 ms total is inside the README ≤120 ms envelope — wording only). [blind]
- Files-changed list omits 4 diff files: `harness/parity.odin`, `tools/ci-local.sh`, `core/sound_events_test.odin`, `app/input/exec_test.odin`. [blind]
- Wire synth lacks the envelope/duration pin the spawn chime got (README ≤120 ms falling-tock contract untested). [tests]
- Live-path `sim_events` wiring in `main.odin:309` is unpinned (nil-safe → silent death; the B1 residual — the emitter is pinned, the wiring isn't). [tests]
- Immediacy AC (~50 ms) remains comment-only/by-construction (r1 N4 remedy accepted + signed off). [tests]
- Debug-overlay tail lines for the two new tags untested (PP_DEBUG-gated, consistent with 12 pre-existing tags). [tests]
- **Advisory test gate: PASS** (P0 100%, P1 ~94%, overall ~82%; lens-executed suites green). [tests]

### Reviewer agreement
- PR body "ALL FOUR kinds" — blind + acceptance
- W5 byte-identity comment false — architecture + codebase

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha.
The loop runs until an APPROVED verdict._
