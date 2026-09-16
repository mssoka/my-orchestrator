# Verification and honest delivery

## Automated evidence

The native workers save/reopen projects, verify real strip ranges/media hashes/cache/colour, and render with Blender. Host FFmpeg is **only** a probe/decoder. Checks include:
- Complete frame/stream decode; exact dimensions, integer fps, frame count and sRGB/Rec709/limited-range metadata.
- All output frames compared with their expected loop phase and adjacent phase candidates at160×90; no stalled adjacent frames. All joins measured, representative sheet retained. This does not certify every full-resolution pixel.
- Native loop endpoint MAD<1/255, genuine unique decoded frames, closure transition relative to adjacent motion. Actual motion/seam judgment still required.
- Original beginning, middle and ending via energy-normalised alignment, at most2-sample offset; correlation>0.98, gain0.98–1.02, no decoded clipping. Select a signal-bearing channel so anti-phase stereo does not cancel the measurement. Silent channels are handled explicitly.
- Original ending covered; frame-grid tail and AAC packet padding recorded separately. A short seek in the middle is insufficient to catch sample-zero MP3 defects. The diagnostic starts at zero and extends to measurable audio; the full export is independently checked.
- Thumbnail decode/dimensions/bit depth, exact selected native phase; loop-only upscale explicitly labelled.
- Input immutability, completed-source-bound resume, failed/partial rejection, safe local ranges and relocated native picture links.

Do not weaken a failing threshold because an export exists. Preserve the attempt and investigate. These thresholds fit this continuous kinetic-loop contract, not every genre of video or intentionally clipped/retimed mix.

## Actual playback and colour

1. Start `mv.py serve`; inspect the actual page, native source UI and thumbnail. Test downloads, responsive layout, Play/pause, restart, native mute/volume, and beginning/seam/middle/ending seeks.
2. Use the installed browser-automation skill/tool. Optionally inject `scripts/playback-probe.js` into the local page. It splits stereo analyser channels and routes **zero gain** to speakers. This is objective audible-content measurement, **not listening**. Reload afterwards for normal audible user playback.
3. Pause and restart, call `nativeMvQA.start()`, then click Play with a real browser gesture. Let the whole delivered file reach `ended`, at rate1, loop disabled, with no seeks/errors/dropped-frame delta. Read `nativeMvQA.result` or `.snapshot()`. Callbacks are not proof of every screen refresh. Preserve failures separately before repeating a test.
4. Compare actual same-frame browser output against the approved loop/native still on the same surface. Avoid mismatched frames or quietly normalizing away a visible difference. Inspect both pixels and measurements; record display/browser limitations.
5. Personally inspect actual beginning, joins, representative/middle and ending frames plus the thumbnail. If listening was not performed, say so explicitly. No calibrated-display, universal-player, beat-grid or HDR claim.
6. Record `review --stage package --note ...` truthfully. Deliver the local page/movie, native kit and thumbnail without an invented approval form or publication. Keep independently delivered production outputs frozen while extracting/testing helpers.

## Validation suite and scope

- `tests/test_contracts.py`: missing/bad input, type/authority/schema checks, changed source/config/helper/finished-file hashes, live lock refusal, partial/failed output rejection, channel/normalised-alignment regression and guarded metadata tests.
- `tests/test_server.py`: actual loopback HTTP, byte/suffix/HEAD ranges, invalid ranges, symlink escape, no upload method, payload tampering.
- `scripts/selftest.py`: neutral native recipe, existing scene intake, approved-loop skip, changed timing/duration, partial final repeat, paths with spaces,44.1/48kHz stereo, native-generated synthetic MP3, real VSE/native export/thumbnail and relocated ZIP reopen. Synthetic decisions are labelled, never real user feedback.
- `tests/discovery.mjs`: installed pi skill loader from a future-job cwd; relative helpers/frontmatter/prompt visibility. It creates no model/session and reloads no active pane. Optional agent-dir argument also verifies default global discovery after stable installation.

See `validation/results.json` for **actual** run coverage and versions. The full-length production evidence was preserved separately and reused, not rerendered to pad this smoke. Generic smoke remains a small technical fixture, not a second music-video commission or automatic-art claim.

Untested OS/GPU/encoder builds, other colour targets/OCIO, VFR/fractional fps, mono/multichannel, alpha/HDR, large buffered exports, special external assets, nonlinear narratives and retiming require separately scoped validation. Bounds in config are not blanket certification.
