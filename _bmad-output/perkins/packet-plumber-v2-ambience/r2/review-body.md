## 🤖 Perkins automated review — round 2

**Job:** packet-plumber-v2-ambience · **Reviewed sha:** c87bf05c · **Reviewers:** 7/7 completed
**Verification:** 24/25 findings confirmed against the code — 1 discarded as false-positive (the `_pr_body_ambience.md`-at-root repeat — established house convention on `v2`)

### Fix audit (r1 → c87bf05)

- **B1 — FIXED, verified mechanically end-to-end.** Ran `tools/build_ambience_loop.py` twice from the vault WAV: both runs produced `ae134e17…405d10`, byte-identical to the committed artifact at HEAD and to the README pin (`-fflags +bitexact -flags:a +bitexact` holds on the pinned ffmpeg 8.0.1 toolchain). The vault input sha256 (`a2417afd…379c`) is asserted with a hard `SystemExit` on mismatch, and the fresh encode's decoded PCM matches the committed artifact's. README now scopes the claim honestly (PCM-stage determinism; byte-identity on the pinned toolchain; decoded-PCM compare across toolchains).
- **W1 — predicate half FIXED, ordering half STILL PRESENT (see Warning 1).** `test_flush_duck_wiring` pins `pending_any_plays` over all four families + empty + staged→duck. But no test executes `audio_flush`, so the trigger-before-clear ordering remains unpinned — while the code/test comments and this PR body now claim it is "unit-pinned". The shipped ordering is correct; the claim is not.
- **W2 — FIXED.** `0.127 peak` now in README.md:68, PR body, spec-ambience-bed.md:179; no "0.4+" figure remains. Re-measured this round: 0.1267 (residual 0.0482) — reproduces exactly.
- **Notes:** N2 (test-count split → 18/18 = 10+8), N3 (parameterized `bed_duck_ratio`, at/below-floor cases pinned), N4 (comment reworded), N6 (numpy documented) all folded. N1 accepted per discipline with documented rationale; N5 partially folded (see Notes).

### Guard bar (r1 bar, re-verified on the new head)

- ✅ Zero golden diffs — no `goldens/`, `demos/`, `core/`, `harness/` paths in the diff; gate 4 (T1 hashes + T2 pixels + replay) green
- ✅ Headless-safe — device early-return intact; `odin test app/audio` → **18/18** green
- ✅ #81 events intact — `Pending` struct, `consumer_consume`, event tags untouched
- ✅ Compressed asset + pinned hash — committed OGG 913,706 B; pin == HEAD bytes == two fresh rebuilds
- ✅ Full suite this round: 18/18 audio · 22/22 app · **11/11 gates** · 48/48 goldens

### Blockers (0)

None.

### Warnings (4)

1. **W1 only half-folded, now with a false "unit-pinned" assurance** [blind, acceptance, architecture, codebase, tests] — `app/audio/audio.odin:396-397`, `audio_test.odin:318-320`, `_pr_body_ambience.md:13`. Moving `flush_maybe_duck(a)` after `a.pending = {}` kills all ducking with 18/18 green; the test drives the helper directly, never `audio_flush`. Fix: fold the pending clear into `flush_maybe_duck` (one pure proc owns check-then-clear), or reword the comments + PR body to claim only predicate/trigger pinning. *Still present since round 1 (ordering half); the overclaim is new.*
2. **Spec Tasks list omits the shipped r2 procs** [blind, codebase] — `spec-ambience-bed.md:104-107`: no `flush_maybe_duck`/`bed_duck_ratio`, and the trigger path is mis-described — the drift class its own change log claims eliminated.
3. **Pause soft-lower wiring unobserved** [tests] — `app/main.odin:502`: `app.mode == .Paused` is the only path feeding `bed_update`'s `paused`, and no test executes the unmuted path. Inverting it ships with all gates green.
4. **Advisory test gate: CONCERNS** [tests] — P0 100%, P1 ≈85%: flush-ordering overclaim + pause-wiring/asset halves manual-only (documented deferrals). Pinning Warning 1 genuinely + a CI asset-integrity line lifts it to PASS.

### Notes (12)

- **N1** [blind] Fifth-family hazard survives (r1 N4 substance): `pending_any_plays` OR-list and the flush's play loops still enumerate the four families separately; a future fifth family must edit both, and no test fails on omission.
- **N2** [blind] `bed_on` gate asymmetry: `bed_update`/`bed_envelope_step`/`bed_duck_trigger` gated, `bed_duck_multiplier`/`bed_level` readers ungated.
- **N3** [blind, edge, codebase] Build script guards every external except a missing `ffmpeg` binary — still a raw `FileNotFoundError` (`shutil.which` + `SystemExit` before line 113).
- **N4** [blind] The 24 MB WAV intermediate is never deleted by the script (`.gitignore` covers commit risk; disk accumulation remains) — `os.remove(OUT_WAV)` after a successful encode.
- **N5** [blind] Regenerated review transcripts still carry terminal chrome (status bars, token counters, absolute paths) — r1 N5's chrome half.
- **N6** [blind] Spec front matter `review_loop_iteration: 0` while its change log records the completed r1 fold.
- **N7** [edge, architecture] Audio-identity DIFFERS branch only prints and exits 0 — after `-y` already overwrote the committed OGG. Encode to temp, compare, move on match (or `SystemExit`).
- **N8** [acceptance] `review-diff.txt` header cites the r1 range `(8a082c8 vs 339e173)` but its content is the r2 tree — stale provenance in the exact class the header says it fixes.
- **N9** [architecture] Build script hard-codes the vault's absolute machine path; env-var/argv override with the pinned sha256 unchanged.
- **N10** [architecture] `paused` parameter (sim-freeze) vs `bed_paused` field (mute mirror) naming collision in the same small API.
- **N11** [tests] No CI integrity/decode gate on the committed OGG — a one-line `shasum` against the README pin closes it (deferral documented in the PR body).
- **N12** [tests] Device-gated init/destroy bed halves (boot fade-in seed, decode-fail unload, stop-before-unload) uncovered — accepted per discipline, documented; optional pure-helper extraction for the boot seed.

### Reviewer agreement

- Warning 1 (flush-ordering overclaim) — independently confirmed by **5 of 7 lenses**; highest-confidence finding of the round.
- Warning 2 (spec drift) — 2 lenses. Note N3 (ffmpeg guard) — 3 lenses. Note N7 (DIFFERS advisory) — 2 lenses.

**Verdict:** READY TO MERGE

Round 1's blocker is gone and mechanically verified; the guard bar is fully green on the new head. The four warnings are coverage-hardening and doc accuracy, not runtime defects — the duck ordering is correct as shipped, and every overclaim is one comment-edit away from honest. Worth one polish pass (Warning 1's reword-or-restructure especially), but nothing here gates the merge.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
