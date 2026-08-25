## 🤖 Perkins automated review — round 1

**Job:** packet-plumber-v2-ambience · **Reviewed sha:** 8a082c8 · **Reviewers:** 7/7 completed
**Verification:** 15/18 defect-claims confirmed against the code — 3 discarded as false-positive; 4 additional guard-bar checks verified PASS mechanically.

**Guard bar:** (a) zero golden diffs ✓ (no `goldens/`, `demos/`, `core/`, `harness/` paths in the diff; `consumer_consume` untouched; the harness mirror never calls `audio_flush`/`bed_update`) · (b) headless-safe ✓ (device early-return gates every raylib audio call; `odin test app/audio` re-run this round: **17/17 green**) · (c) layers beside #81 ✓ (duck trigger appended after the four play loops; `Pending`/event tags untouched) · (d) asset compressed+sha256-pinned ✓ (913,706-byte OGG, hash matches the pin; WAV never committed) **but transform reproducibility ✗ — see blocker.**

### Blockers (1)

1. **Documented "byte-identical rebuild" is false — the vorbis encode is non-deterministic, and the vault input is never hashed** [codebase + Perkins mechanical] · `tools/build_ambience_loop.py:96` + `assets/audio/README.md:98-100`
   The README/PR body claim the script "re-builds the committed OGG byte-identically". I re-ran it this round: the PCM stage **is** deterministic (the 0.048 wrap residual reproduced exactly at 0.0482 — that claim is honest), but the OGG bytes are **not**: three identical control encodes of the same PCM on this machine produced three different sha256s (same 913,706 bytes each — the ffmpeg native vorbis encoder, `-c:a vorbis -strict -2`, is non-deterministic run-to-run; this homebrew build ships no libvorbis). The script's only `hashlib` call hashes the output; the input vault WAV is never hashed anywhere.
   **Fix:** hash + print the vault input sha256 beside the output; make the encode deterministic (pinned ffmpeg build/container or a deterministic encoder path) and re-pin — or reword the docs to "PCM stage deterministic; committed artifact sha256-pinned; rebuild verified by decode-compare (duration + decoded-PCM hash), not byte-identity".

### Warnings (2)

1. **Duck-trigger wiring has no test: `pending_any_plays` and its flush call-site ordering are unpinned** [tests] · `app/audio/audio.odin:398`
   Moving the trigger after `a.pending = {}` or dropping a family from the OR-list kills ducking silently — all 17 tests stay green. The predicate is pure and headless-testable. **Fix:** add a unit test driving `pending_any_plays` over each family.
2. **The "0.4+ amplitude" hard-cut figure does not reproduce — actual hard-cut wrap jump at the documented window is 0.127 peak** [acceptance + Perkins recompute] · `assets/audio/README.md:67-68` (also `_pr_body_ambience.md`, `spec-ambience-bed.md:179`)
   Recomputed from the vault WAV with the script's own math: pre-crossfade wrap jump at [41.4s, 167.0s] = **0.1267** peak — the docs overstate it >3×. The design conclusion (crossfade needed) still holds — 0.127 ≫ 0.048 — but the documented number is wrong. **Fix:** replace "0.4+ amplitude" with the measured ~0.13 in all three docs.

### Notes (7)

1. **Device-gated halves never executed by tests** [tests] · `app/audio/audio.odin:208` — `audio_init`'s no-device path, `load_bed` branches, boot fade-in seeding, destroy stop/unload run only structurally guarded (matches the #81 precedent; structural risk only). Optional: a CI smoke step booting the app with no audio device, asserting exit 0.
2. **PR body test-count split wrong: "13 pre-existing + 4 new bed tests" — actual 10 + 7** [acceptance, blind, codebase, tests] · `_pr_body_ambience.md:47` — the 17/17 headline is correct and was verified green this round; only the parenthetical is stale.
3. **`test_bed_duck_never_raises` cannot fail at the shipped constants** [blind] · `app/audio/audio_test.odin:300` — uncapped ratio is 0.3, so the cap is not load-bearing in the test; deleting it keeps all tests green until the master is retuned at/below the duck level. Fix: parameterize the multiplier over master/duck volumes so the master-below-duck case is driven directly.
4. **`pending_any_plays` comment overpromises single-source** [blind, codebase] · `app/audio/audio.odin:553` — the flush's play loops do not key off the helper; a fifth family still requires editing both. Code correct today; comment misstates the invariant.
5. **Committed `review-diff.txt` is a stale pre-fold snapshot contradicting the shipped code** [architecture, blind] · `_bmad-output/reviews/v2-ambience/review-diff.txt:211` — shows the uncapped duck multiplier the shipped code caps (its sibling `verif-gap.txt` admits the staleness); regenerate from the final tree or label it as the pre-r1 snapshot, and strip session chrome.
6. **Undocumented numpy dependency** [codebase] · `tools/build_ambience_loop.py:31` — the docstring/README document only ffmpeg; add "Requires python3 + numpy".
7. **Advisory test gate: PASS** [tests] — P0 100%, P1 ~95%, overall ~90% (goldens byte-identical; consumer untouched; only device-gated init halves partial, precedent-matching).

### Reviewer agreement

- PR-body test split wrong — **4 lenses** (acceptance, blind, codebase, tests)
- `pending_any_plays` comment overpromise — 2 lenses (blind, codebase)
- Stale committed `review-diff.txt` — 2 lenses (architecture, blind)

**Rejected as false-positive (3):** "duck staged during mute dips after unmute" (impossible — `audio_flush` early-returns on `muted`, `bed_duck_trigger` unreachable); "bed device-gate implemented nowhere" (the gate is structural: `load_bed`'s only caller sits after the `!device_on` early return); "`_pr_body_ambience.md` at root is unprecedented scratch" (v2 already tracks four `_pr_body_*.md` files).

**Claims spot-check (per the briefing):** loop residual 0.048 — **honest** (reproduced 0.0482); hard-cut 0.4+ — **false** (0.127, warning 2); duck envelope 0.30s→0.12 + 0.60s ramp, relative + capped — **verified in code**; 17/17 audio tests — **verified green** (re-run); 11 gates — consistent (GATES array has 11 entries); 48/48 demos — 48 `.dem` files counted, harness run not re-executed this round (structural verification only: zero sim/harness/golden changes).

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
