## 🤖 Perkins automated review — round 3
**Job:** packet-plumber-v2-font-overhaul · **Reviewed sha:** abec50b · **Reviewers:** 7/7 completed
**Verification:** 18/18 unique findings confirmed against the code — 0 discarded as false-positive

### Fix audit (r1 → r3) — 22 prior findings
**Fixed (13):** B1 fail-loud loader (reports end-to-end, zero `GetFontDefault` coercion, all three call sites refuse, data-stage pin bites) · B2 PR body (font job's content; T1/replay proof + re-bless cause + before/after pointers on the body) · W1 screenshot order (post-flush) · W2 glyph-probe value lookup · W3 baseline → committed font · W4 replay-loop dedup · W5 tabular pin (r1's option B) · N3 `MemFree(fg)` · N4 `[96]rune` cap · N5 palette fallbacks synced · N6/N7/N8 size-ladder unifications · N12 body ink_soft wording · N14 palcheck guard.
**Partial (4):** N1 (SLA row 14 vs shipped 17) · N2 (six stale-comment sites remain) · N13 (era-stale clearance comment) · W5 (wiring residual, below).
**Not folded (4):** N9 gallery global · N10 PP_SW_AUDIO producer · N15 debug smoke — all claimed folded under "N1–N15".
**Fictitious (1):** N11 — see Blocker 1.

### Blockers (2)
**1. The N11 fold is fictitious — the gallery retry budget is dead code** · `app/gallery.odin:57` + re-arm sites 240–284 · [7/7 reviewers]
`retries: int, // N11: the condition-poll frame budget (GALLERY_MAX_RETRIES)` — repo-wide grep returns **only this line**: no `GALLERY_MAX_RETRIES` exists, the field is never read, and the stage machine still re-arms `gallery.wait` unbounded at 8 sites. The commit claims N11 folded; it is not. *Fix: implement the budget (abort with stage name at the cap) or delete the field and retract the claim.*

**2. The audio seam refactor deleted `rl.CloseAudioDevice()` instead of wrapping it** · `app/audio/audio.odin:316-331` · [6/7 reviewers]
Pre-refactor (`origin/v2`): `audio_destroy` ends with an unconditional `rl.CloseAudioDevice()`. Post-refactor: **zero hits repo-wide** — the device is never closed, while the proc comment still says "unload the sounds + **close the device**". The seam was ruled in as behavior-preserving (#86's teardown idioms); this is a real teardown behavior change — the exact delta-introduced class this round hunts. *Fix: add `audio_close_device()` to the seam and call it at the end of `audio_destroy`.*

### Warnings (5)
- **N10 unfixed, aggravated** [6/7]: the seam comment claims "the producer is the gallery build documented in `app/gallery.odin`" — no such documentation exists; PP_SW_AUDIO still has zero in-repo producers; the SW app build remains irreproducible.
- **PR body stale post-#88 rebase** [acceptance]: line 27 still says the branch "sits on the settled v2 head 339e173" (actual base: post-#88 `ef41b6c`); the combined font+sculpt re-bless cause lives only in the commit message — rule 6's cause documentation should be on the merge surface.
- **B1 exit path untested** [tests]: the pin covers the data stage; nothing automates "missing asset → exit 2" through `load_font_file`/`load_fonts` and the three `os.exit(2)` wrappers (a re-coercion after the data stage would pass the pin).
- **W5 wiring residual** [tests]: the tabular-advance pin holds, but no automated check *draws* the NOC overlay — a `draw_mono_c` wiring regression passes all 11 gates.
- **Advisory test gate: CONCERNS** [tests]: P0 covered; P1 partial on the two gaps above + app text surfaces (note 6).

### Notes (11)
N2 stale-comment cluster (font_check ladder docstring 22/30 vs shipped 24/32, the now-false rune-truncation claims in font_check + `tools/lint.sh` gate-6, deleted `load_hud_font` ref, crisis "14px" over a 15px draw, noc_row "≥14/10" ladder) · N1 residual (specimen SLA 14 vs shipped 17) · N9 gallery global still undocumented · N13 era-stale clearance comment · N15 compile-only debug gate · B1 residual: unreadable **fallback** asset returns ok silently (⚠ absent; CI pin is the only net) · W1 residual: identical when/else `EndDrawing` + false "Release builds carry nothing" · A/B tooling swaps body font only (headers/NOC stay Plex in candidate captures) · HUD/QoS/settings/tray/popover text surfaces have no automated pixel coverage · `audio_flush` replacements misindented (4 sites) · font_test probes leak the merged glyph block (test-side).

### Reviewer agreement
F1 N11 fictitious fold (7 sources) · F2 CloseAudioDevice dropped (6) · N10 dangling doc (6) · N2 stale comments (5) · N9 gallery global (3).

**Verdict:** NEEDS CHANGES

Mechanical guards this round (run natively by Perkins on `abec50b`): **11/11 gates green** — harness 48/48 (T1 + T2 + replay bit-for-bit), drift-check 345 mutations rejected, input parity 27 scenarios, core 236/236, render 56/56 incl. the 4 font pins, palcheck green on the sculpt re-pin. No aesthetic judgments (non-k3 round — pixel checks mechanical only).

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
